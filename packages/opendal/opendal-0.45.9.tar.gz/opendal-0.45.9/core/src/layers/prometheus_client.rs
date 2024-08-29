// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

use std::fmt;
use std::fmt::Debug;
use std::sync::Arc;
use std::time::Duration;
use std::time::Instant;

use bytes::Buf;
use prometheus_client::encoding::EncodeLabel;
use prometheus_client::encoding::EncodeLabelSet;
use prometheus_client::encoding::LabelSetEncoder;
use prometheus_client::metrics::counter::Counter;
use prometheus_client::metrics::family::Family;
use prometheus_client::metrics::histogram;
use prometheus_client::metrics::histogram::Histogram;
use prometheus_client::registry::Registry;

use crate::raw::Access;
use crate::raw::*;
use crate::*;

/// Add [prometheus-client](https://docs.rs/prometheus-client) for every operation.
///
/// # Examples
///
/// ```no_build
/// use log::debug;
/// use log::info;
/// use opendal::layers::PrometheusClientLayer;
/// use opendal::services;
/// use opendal::Operator;
/// use opendal::Result;
///
/// /// Visit [`opendal::services`] for more service related config.
/// /// Visit [`opendal::Operator`] for more operator level APIs.
/// #[tokio::main]
/// async fn main() -> Result<()> {
///     // Pick a builder and configure it.
///     let builder = services::Memory::default();
///     let mut registry = prometheus_client::registry::Registry::default();
///
///     let op = Operator::new(builder)
///         .expect("must init")
///         .layer(PrometheusClientLayer::new(&mut registry))
///         .finish();
///     debug!("operator: {op:?}");
///
///     // Write data into object test.
///     op.write("test", "Hello, World!").await?;
///     // Read data from object.
///     let bs = op.read("test").await?;
///     info!("content: {}", String::from_utf8_lossy(&bs.to_bytes()));
///
///     // Get object metadata.
///     let meta = op.stat("test").await?;
///     info!("meta: {:?}", meta);
///
///     // Export prometheus metrics.
///     let mut buf = String::new();
///     prometheus_client::encoding::text::encode(&mut buf, &registry).unwrap();
///     println!("## Prometheus Metrics");
///     println!("{}", buf);
///     Ok(())
/// }
/// ```
#[derive(Clone, Debug)]
pub struct PrometheusClientLayer {
    metrics: PrometheusClientMetricDefinitions,
}

impl PrometheusClientLayer {
    /// Create PrometheusClientLayer while registering itself to this registry. Please keep in caution
    /// that do NOT call this method multiple times with a same registry. If you want to initialize multiple
    /// [`PrometheusClientLayer`] with a single registry, you should use [`Arc::clone`] instead.
    pub fn new(registry: &mut Registry) -> Self {
        let metrics = PrometheusClientMetricDefinitions::register(registry);
        Self { metrics }
    }
}

impl<A: Access> Layer<A> for PrometheusClientLayer {
    type LayeredAccess = PrometheusClientAccessor<A>;

    fn layer(&self, inner: A) -> Self::LayeredAccess {
        let meta = inner.info();
        let scheme = meta.scheme();
        let root = meta.root().to_string();
        let name = meta.name().to_string();

        let defs = Arc::new(self.metrics.clone());
        let metrics = PrometheusClientMetrics::new(defs, scheme, root, name);
        PrometheusClientAccessor { inner, metrics }
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Hash)]
struct OperationLabels {
    op: &'static str,
    scheme: &'static str,
    root: Arc<String>,
    namespace: Arc<String>,
}

impl EncodeLabelSet for OperationLabels {
    fn encode(&self, mut encoder: LabelSetEncoder) -> Result<(), fmt::Error> {
        ("op", self.op).encode(encoder.encode_label())?;
        ("scheme", self.scheme).encode(encoder.encode_label())?;
        ("root", self.root.as_str()).encode(encoder.encode_label())?;
        ("namespace", self.namespace.as_str()).encode(encoder.encode_label())?;
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Hash)]
struct ErrorLabels {
    op: &'static str,
    scheme: &'static str,
    root: Arc<String>,
    namespace: Arc<String>,
    error: &'static str,
}

impl EncodeLabelSet for ErrorLabels {
    fn encode(&self, mut encoder: LabelSetEncoder) -> Result<(), fmt::Error> {
        ("op", self.op).encode(encoder.encode_label())?;
        ("scheme", self.scheme).encode(encoder.encode_label())?;
        ("root", self.root.as_str()).encode(encoder.encode_label())?;
        ("namespace", self.namespace.as_str()).encode(encoder.encode_label())?;
        ("error", self.error).encode(encoder.encode_label())?;
        Ok(())
    }
}

/// [`PrometheusClientMetricDefinitions`] provide the definition about RED(Rate/Error/Duration) metrics with the `prometheus-client` crate.
#[derive(Debug, Clone)]
struct PrometheusClientMetricDefinitions {
    /// Total times of the specific operation be called.
    requests_total: Family<OperationLabels, Counter>,
    /// Total times of the specific operation be called but meet error.
    errors_total: Family<ErrorLabels, Counter>,
    /// Latency of the specific operation be called.
    request_duration_seconds: Family<OperationLabels, Histogram>,

    /// Total size of bytes.
    bytes_total: Family<OperationLabels, Counter>,
    /// The size of bytes.
    bytes: Family<OperationLabels, Histogram>,
}

impl PrometheusClientMetricDefinitions {
    pub fn register(registry: &mut Registry) -> Self {
        let requests_total = Family::default();
        let errors_total = Family::default();
        let request_duration_seconds = Family::<OperationLabels, _>::new_with_constructor(|| {
            let buckets = histogram::exponential_buckets(0.01, 2.0, 16);
            Histogram::new(buckets)
        });

        let bytes_total = Family::default();
        let bytes = Family::<OperationLabels, _>::new_with_constructor(|| {
            let buckets = histogram::exponential_buckets(1.0, 2.0, 16);
            Histogram::new(buckets)
        });

        registry.register(
            "opendal_requests",
            "Total times of the specific operation be called",
            requests_total.clone(),
        );
        registry.register(
            "opendal_errors",
            "Total times of the specific operation be called but meet error",
            errors_total.clone(),
        );
        registry.register(
            "opendal_request_duration_seconds",
            "Latency of the specific operation be called",
            request_duration_seconds.clone(),
        );

        registry.register("opendal_bytes", "Total size of bytes", bytes_total.clone());
        registry.register("opendal_bytes", "The size of bytes", bytes.clone());

        Self {
            requests_total,
            errors_total,
            request_duration_seconds,
            bytes_total,
            bytes,
        }
    }
}

#[derive(Clone, Debug)]
struct PrometheusClientMetrics {
    metrics: Arc<PrometheusClientMetricDefinitions>,
    scheme: Scheme,
    root: Arc<String>,
    name: Arc<String>,
}

impl PrometheusClientMetrics {
    fn new(
        metrics: Arc<PrometheusClientMetricDefinitions>,
        scheme: Scheme,
        root: String,
        name: String,
    ) -> Self {
        Self {
            metrics,
            scheme,
            root: Arc::new(root),
            name: Arc::new(name),
        }
    }

    fn increment_request_total(&self, labels: &OperationLabels) {
        self.metrics.requests_total.get_or_create(labels).inc();
    }

    fn increment_errors_total(&self, op: Operation, err: ErrorKind) {
        let labels = self.gen_error_labels(op, err);
        self.metrics.errors_total.get_or_create(&labels).inc();
    }

    fn observe_request_duration(&self, labels: &OperationLabels, duration: Duration) {
        self.metrics
            .request_duration_seconds
            .get_or_create(labels)
            .observe(duration.as_secs_f64());
    }

    fn observe_bytes_total(&self, labels: &OperationLabels, bytes: usize) {
        self.metrics
            .bytes_total
            .get_or_create(labels)
            .inc_by(bytes as u64);
        self.metrics
            .bytes
            .get_or_create(labels)
            .observe(bytes as f64);
    }

    fn gen_operation_labels(&self, op: Operation) -> OperationLabels {
        OperationLabels {
            op: op.into_static(),
            scheme: self.scheme.into_static(),
            root: self.root.clone(),
            namespace: self.name.clone(),
        }
    }

    fn gen_error_labels(&self, op: Operation, err: ErrorKind) -> ErrorLabels {
        ErrorLabels {
            op: op.into_static(),
            scheme: self.scheme.into_static(),
            root: self.root.clone(),
            namespace: self.name.clone(),
            error: err.into_static(),
        }
    }
}

#[derive(Clone)]
pub struct PrometheusClientAccessor<A: Access> {
    inner: A,
    metrics: PrometheusClientMetrics,
}

impl<A: Access> Debug for PrometheusClientAccessor<A> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("PrometheusAccessor")
            .field("inner", &self.inner)
            .finish_non_exhaustive()
    }
}

impl<A: Access> LayeredAccess for PrometheusClientAccessor<A> {
    type Inner = A;
    type Reader = PrometheusClientMetricWrapper<A::Reader>;
    type BlockingReader = PrometheusClientMetricWrapper<A::BlockingReader>;
    type Writer = PrometheusClientMetricWrapper<A::Writer>;
    type BlockingWriter = PrometheusClientMetricWrapper<A::BlockingWriter>;
    type Lister = A::Lister;
    type BlockingLister = A::BlockingLister;

    fn inner(&self) -> &Self::Inner {
        &self.inner
    }

    async fn create_dir(&self, path: &str, args: OpCreateDir) -> Result<RpCreateDir> {
        let op = Operation::CreateDir;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.create_dir(path, args).await;
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    async fn read(&self, path: &str, args: OpRead) -> Result<(RpRead, Self::Reader)> {
        let op = Operation::Read;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.read(path, args).await;
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        match result {
            Ok((rp, r)) => Ok((
                rp,
                PrometheusClientMetricWrapper::new(r, self.metrics.clone()),
            )),
            Err(err) => {
                self.metrics.increment_errors_total(op, err.kind());
                Err(err)
            }
        }
    }

    async fn write(&self, path: &str, args: OpWrite) -> Result<(RpWrite, Self::Writer)> {
        let op = Operation::Write;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.write(path, args).await;
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        match result {
            Ok((rp, w)) => Ok((
                rp,
                PrometheusClientMetricWrapper::new(w, self.metrics.clone()),
            )),
            Err(err) => {
                self.metrics.increment_errors_total(op, err.kind());
                Err(err)
            }
        }
    }

    async fn stat(&self, path: &str, args: OpStat) -> Result<RpStat> {
        let op = Operation::Stat;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.stat(path, args).await;
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    async fn delete(&self, path: &str, args: OpDelete) -> Result<RpDelete> {
        let op = Operation::Delete;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.delete(path, args).await;
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    async fn list(&self, path: &str, args: OpList) -> Result<(RpList, Self::Lister)> {
        let op = Operation::List;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.list(path, args).await;
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    async fn batch(&self, args: OpBatch) -> Result<RpBatch> {
        let op = Operation::Batch;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.batch(args).await;
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    async fn presign(&self, path: &str, args: OpPresign) -> Result<RpPresign> {
        let op = Operation::Presign;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.presign(path, args).await;
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    fn blocking_create_dir(&self, path: &str, args: OpCreateDir) -> Result<RpCreateDir> {
        let op = Operation::BlockingCreateDir;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.blocking_create_dir(path, args);
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    fn blocking_read(&self, path: &str, args: OpRead) -> Result<(RpRead, Self::BlockingReader)> {
        let op = Operation::BlockingRead;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let result = self.inner.blocking_read(path, args).map(|(rp, r)| {
            (
                rp,
                PrometheusClientMetricWrapper::new(r, self.metrics.clone()),
            )
        });

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    fn blocking_write(&self, path: &str, args: OpWrite) -> Result<(RpWrite, Self::BlockingWriter)> {
        let op = Operation::BlockingWrite;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let result = self.inner.blocking_write(path, args).map(|(rp, r)| {
            (
                rp,
                PrometheusClientMetricWrapper::new(r, self.metrics.clone()),
            )
        });

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    fn blocking_stat(&self, path: &str, args: OpStat) -> Result<RpStat> {
        let op = Operation::BlockingList;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.blocking_stat(path, args);
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    fn blocking_delete(&self, path: &str, args: OpDelete) -> Result<RpDelete> {
        let op = Operation::BlockingDelete;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.blocking_delete(path, args);
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }

    fn blocking_list(&self, path: &str, args: OpList) -> Result<(RpList, Self::BlockingLister)> {
        let op = Operation::BlockingList;
        let labels = self.metrics.gen_operation_labels(op);

        self.metrics.increment_request_total(&labels);

        let start = Instant::now();
        let result = self.inner.blocking_list(path, args);
        self.metrics
            .observe_request_duration(&labels, start.elapsed());

        result.map_err(|err| {
            self.metrics.increment_errors_total(op, err.kind());
            err
        })
    }
}

pub struct PrometheusClientMetricWrapper<R> {
    inner: R,
    metrics: PrometheusClientMetrics,
}

impl<R> PrometheusClientMetricWrapper<R> {
    fn new(inner: R, metrics: PrometheusClientMetrics) -> Self {
        Self { inner, metrics }
    }
}

impl<R: oio::Read> oio::Read for PrometheusClientMetricWrapper<R> {
    async fn read(&mut self) -> Result<Buffer> {
        let op = Operation::ReaderRead;
        let labels = self.metrics.gen_operation_labels(op);

        let start = Instant::now();

        match self.inner.read().await {
            Ok(bs) => {
                self.metrics.observe_bytes_total(&labels, bs.remaining());
                self.metrics
                    .observe_request_duration(&labels, start.elapsed());
                Ok(bs)
            }
            Err(err) => {
                self.metrics.increment_errors_total(op, err.kind());
                Err(err)
            }
        }
    }
}

impl<R: oio::BlockingRead> oio::BlockingRead for PrometheusClientMetricWrapper<R> {
    fn read(&mut self) -> Result<Buffer> {
        let op = Operation::BlockingReaderRead;
        let labels = self.metrics.gen_operation_labels(op);

        let start = Instant::now();

        self.inner
            .read()
            .map(|bs| {
                self.metrics.observe_bytes_total(&labels, bs.remaining());
                self.metrics
                    .observe_request_duration(&labels, start.elapsed());
                bs
            })
            .map_err(|err| {
                self.metrics.increment_errors_total(op, err.kind());
                err
            })
    }
}

impl<R: oio::Write> oio::Write for PrometheusClientMetricWrapper<R> {
    async fn write(&mut self, bs: Buffer) -> Result<()> {
        let op = Operation::WriterWrite;
        let labels = self.metrics.gen_operation_labels(op);

        let start = Instant::now();
        let size = bs.len();

        self.inner
            .write(bs)
            .await
            .map(|_| {
                self.metrics.observe_bytes_total(&labels, size);
                self.metrics
                    .observe_request_duration(&labels, start.elapsed());
            })
            .map_err(|err| {
                self.metrics.increment_errors_total(op, err.kind());
                err
            })
    }

    async fn close(&mut self) -> Result<()> {
        let op = Operation::WriterClose;
        let labels = self.metrics.gen_operation_labels(op);

        let start = Instant::now();

        self.inner
            .close()
            .await
            .map(|_| {
                self.metrics
                    .observe_request_duration(&labels, start.elapsed());
            })
            .map_err(|err| {
                self.metrics.increment_errors_total(op, err.kind());
                err
            })
    }

    async fn abort(&mut self) -> Result<()> {
        let op = Operation::WriterAbort;
        let labels = self.metrics.gen_operation_labels(op);

        let start = Instant::now();

        self.inner
            .abort()
            .await
            .map(|_| {
                self.metrics
                    .observe_request_duration(&labels, start.elapsed());
            })
            .map_err(|err| {
                self.metrics.increment_errors_total(op, err.kind());
                err
            })
    }
}

impl<R: oio::BlockingWrite> oio::BlockingWrite for PrometheusClientMetricWrapper<R> {
    fn write(&mut self, bs: Buffer) -> Result<()> {
        let op = Operation::BlockingWriterWrite;
        let labels = self.metrics.gen_operation_labels(op);

        let start = Instant::now();
        let size = bs.len();

        self.inner
            .write(bs)
            .map(|_| {
                self.metrics.observe_bytes_total(&labels, size);
                self.metrics
                    .observe_request_duration(&labels, start.elapsed());
            })
            .map_err(|err| {
                self.metrics.increment_errors_total(op, err.kind());
                err
            })
    }

    fn close(&mut self) -> Result<()> {
        let op = Operation::BlockingWriterClose;
        let labels = self.metrics.gen_operation_labels(op);

        let start = Instant::now();

        self.inner
            .close()
            .map(|_| {
                self.metrics
                    .observe_request_duration(&labels, start.elapsed());
            })
            .map_err(|err| {
                self.metrics.increment_errors_total(op, err.kind());
                err
            })
    }
}
