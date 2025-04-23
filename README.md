# Atlan Cloud Cost Tracker (CCT)

## Overview

This project implements a comprehensive cloud cost optimization system designed to address the challenges of monitoring, analyzing, and optimizing cloud expenses across multiple providers in real-time. The architecture provides a solution to three critical problems:

1. Detecting cost increases with minimal delay
2. Accurately identifying the sources of cost spikes
3. Providing clear paths for cost optimization

The system continuously collects cost data from AWS, Azure, and GCP, detects anomalies in real-time, and implements automated cost optimization workflows while maintaining policy compliance.

## Architecture

### Architecture Diagram

![Architecture Diagram](atlan1.png)

### Sequence Diagram

![Sequence Diagram](Atlanseq.png)

## System Components

The architecture integrates several specialized components to create a complete cost optimization pipeline:

### Data Collection Layer

- **Cloud Providers (AWS, Azure, GCP)**: Source systems generating resource utilization and cost data.
- **Fluent Bit Log Processor**: Collects resource logs from all cloud providers every 5 seconds and normalizes formats.


### Storage \& Monitoring Layer

- **VictoriaMetrics Time-Series DB**: Efficiently stores high-volume time-series cost data from all providers.
- **AlertManager**: Checks metrics every 3 seconds for anomalies and generates alerts when thresholds are exceeded.


### Automation Layer

- **Apache Kafka Event Stream**: Central messaging backbone that handles cost anomaly events.
- **Argo Workflows**: Orchestration engine that consumes events and automates optimization processes.
- **AdmissionController**: Validates all proposed optimization actions against organizational policies.


### Security Layer

- **HashiCorp Vault**: Securely manages credentials for accessing cloud provider APIs.


### Analysis \& Visualization Layer

- **PostgreSQL**: Stores metadata about optimization activities and results.
- **Grafana Dashboards**: Provides visualization of cost trends and optimization outcomes.


### Alerting Integration

- **Zenduty**: Provides incident management for human notification when needed.


## How It Works

The system operates through three continuous loops:

### 1. Data Collection Loop (every 5 seconds)

```
Cloud Providers → Fluent Bit → VictoriaMetrics
```

- Cloud providers generate resource logs containing cost information
- Fluent Bit collects and processes these logs into a consistent format
- Processed logs are stored in VictoriaMetrics time-series database


### 2. Anomaly Detection Loop (every 3 seconds)

```
VictoriaMetrics → AlertManager → Kafka/Zenduty
```

- AlertManager checks metrics in VictoriaMetrics for anomalies
- When detected, alerts are sent to Kafka for automated processing
- Critical incidents are also created in Zenduty for human notification


### 3. Optimization Loop (continuous)

```
Kafka → Argo Workflows → AdmissionController → Cloud Providers
```

- Argo Workflows consumes anomaly events from Kafka
- Workflows prepare optimization plans (e.g., rightsizing, cleanup)
- AdmissionController validates plans against policies
- Approved optimizations are executed against cloud providers
- Results are stored in PostgreSQL for future reference


## Cost Optimization Workflows

The system implements several types of optimization workflows:

### Resource Rightsizing

```
When: Instance CPU utilization &lt; 20% for 14+ days
Action: Downsize compute instances to appropriate size
Example: EC2 m5.xlarge → m5.large ($87.60/month savings)
```


### Idle Resource Cleanup

```
When: Storage volumes unattached for 30+ days
Action: Snapshot and delete unused volumes
Example: 12 unattached EBS volumes ($43.20/month savings)
```


### Reserved Instance Optimization

```
When: On-demand usage pattern stable for 60+ days
Action: Purchase appropriate Savings Plans
Example: 1-year commitment (24% savings on eligible compute)
```


### Storage Lifecycle Management

```
When: S3/Blob data accessed &lt; 5% in 90 days
Action: Move to lower-cost storage tiers
Example: Standard → Infrequent Access (40% storage cost reduction)
```


## Project Structure

### Files and Artifacts

- **Atlan_seq.png**
    - Sequence diagram showing the three main loops of the system
    - Illustrates timing intervals and interactions between components
- **Atlan.png**
    - Architecture diagram showing all components and data flows
    - Provides a visual representation of the complete system
- **documentation.pdf**
    - Comprehensive explanation of design decisions and trade-offs
    - Detailed component descriptions and interaction patterns
    - Proof of solution addressing the stated problems
- **demo.py**
    - Python simulation of the complete system
    - Demonstrates all three loops in action
    - Includes sample cost data and optimization workflows


## How to Run the Demo

### Prerequisites

- Python 3.7 or higher
- Docker and Docker Compose (for running containerized components)
- Basic understanding of cloud provider billing APIs


### Installation Steps

1. Clone this repository:

```bash
git clone https://github.com/Maniac1769/AtlanCCT.git
cd AtlanCCT
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure cloud provider credentials in `.env` file
4. Start the system:

```bash
python demo.py
```


### Example Output

```
📊 [Fluent Bit] Collecting logs from AWS, Azure, GCP
📊 [VictoriaMetrics] Stored AWS compute cost: $523.45
🚨 [AlertManager] Cost anomaly detected! AWS compute $523.45 (79.6% above baseline)
🔁 [Kafka] Producing event: {provider: "AWS", service: "EC2", deviation: 79.6%}
⚙️ [Argo Workflows] Starting compute-optimization workflow
🔒 [AdmissionController] Policy validation passed
📉 [Argo Workflows] Rightsizing complete: $523.45 → $418.76 (20% reduction)
```


## System Benefits

- **Real-Time Detection**: Identifies cost anomalies within seconds instead of days or weeks
- **Clear Attribution**: Pinpoints exactly which resources are driving cost increases
- **Automated Optimization**: Implements cost-saving measures without manual intervention
- **Policy Compliance**: Ensures all optimizations follow organizational guidelines
- **Comprehensive Visibility**: Provides dashboards and historical data for all cost activities


## Future Enhancements

- Machine learning-based anomaly detection to replace static thresholds
- Predictive cost forecasting to anticipate future spending
- Integration with infrastructure as code systems for preventative optimization
- Enhanced multi-cloud optimization strategies


## License

This project is licensed under the MIT License - see the LICENSE file for details.
