"""
Cloud Cost Optimization Demo - High-Level Workflow Simulation
Components Modeled:
- Cloud APIs (AWS/Azure/GCP)
- VictoriaMetrics (TSDB)
- Apache Kafka (Event Stream)
- Argo Workflows (Automation)
- Alertmanager (Alerting)
"""

import asyncio
import random
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Configuration
class CloudProvider(Enum):
    AWS = 1
    AZURE = 2
    GCP = 3

COST_THRESHOLDS = {
    CloudProvider.AWS: 500,
    CloudProvider.AZURE: 450,
    CloudProvider.GCP: 400
}
KAFKA_TOPIC = "cost-events"
ARGOWORKFLOW_OPTIMIZATION_MAP = {
    "compute": "argo-workflow-compute-optimization",
    "storage": "argo-workflow-storage-cleanup"
}

@dataclass
class CostMetric:
    timestamp: datetime
    provider: CloudProvider
    service: str
    cost: float
    tags: dict

class CostMonitor:
    """Simulates VictoriaMetrics integration and cost data collection"""
    
    def __init__(self):
        self.metrics = []
    
    async def collect_metrics(self):
        """Simulate periodic metric collection from cloud providers"""
        while True:
            for provider in CloudProvider:
                cost = random.uniform(300, 600)  # Simulated API call
                metric = CostMetric(
                    timestamp=datetime.now(),
                    provider=provider,
                    service=random.choice(["compute", "storage", "database"]),
                    cost=cost,
                    tags={"environment": "prod", "team": random.choice(["team-a", "team-b"])}
                )
                self.metrics.append(metric)
                print(f"📊 [VictoriaMetrics] Stored {provider.name} {metric.service} cost: ${cost:.2f}")
            await asyncio.sleep(5)

class AnomalyDetector:
    """Simulates anomaly detection and Kafka event production"""
    
    def __init__(self, cost_monitor: CostMonitor):
        self.cost_monitor = cost_monitor
        self.kafka_events = []
    
    async def analyze_metrics(self):
        """Check for cost anomalies and produce Kafka events"""
        while True:
            latest_metrics = self.cost_monitor.metrics[-3:]  # Get last 3 metrics
            for metric in latest_metrics:
                threshold = COST_THRESHOLDS[metric.provider]
                if metric.cost > threshold:
                    event = {
                        "timestamp": metric.timestamp.isoformat(),
                        "provider": metric.provider.name,
                        "service": metric.service,
                        "cost": metric.cost,
                        "threshold": threshold,
                        "tags": metric.tags
                    }
                    self.kafka_events.append(event)
                    print(f"🚨 [AlertManager] Cost anomaly detected! {event}")
                    await self.trigger_kafka_event(event)
            await asyncio.sleep(3)

    async def trigger_kafka_event(self, event):
        """Simulate Kafka event production"""
        print(f"🔁 [Kafka] Producing event to '{KAFKA_TOPIC}': {event}")
        # In real implementation: kafka_producer.send(KAFKA_TOPIC, value=event)

class ArgoWorkflowOrchestrator:
    """Simulates Argo Workflows automation"""
    
    def __init__(self, anomaly_detector: AnomalyDetector):
        self.anomaly_detector = anomaly_detector
    
    async def listen_for_events(self):
        """Simulate event consumption from Kafka"""
        while True:
            if self.anomaly_detector.kafka_events:
                event = self.anomaly_detector.kafka_events.pop(0)
                await self.trigger_optimization_workflow(event)
            await asyncio.sleep(1)

    async def trigger_optimization_workflow(self, event):
        """Simulate Argo Workflow execution"""
        workflow_type = ARGOWORKFLOW_OPTIMIZATION_MAP.get(event["service"], "default")
        print(f"⚙️ [Argo Workflows] Starting {workflow_type} for {event['provider']} {event['service']}")
        print(f"   📉 Cost before: ${event['cost']:.2f}")
        optimized_cost = event["cost"] * 0.8  # Simulate 20% reduction
        print(f"   📈 Optimized cost: ${optimized_cost:.2f}")
        # Simulate Admission Controller policy check
        print("🔒 [Admission Controller] Policy validation passed")

async def main():
    """Run the complete simulation"""
    cost_monitor = CostMonitor()
    anomaly_detector = AnomalyDetector(cost_monitor)
    workflow_orchestrator = ArgoWorkflowOrchestrator(anomaly_detector)

    # Start all components
    tasks = [
        cost_monitor.collect_metrics(),
        anomaly_detector.analyze_metrics(),
        workflow_orchestrator.listen_for_events()
    ]
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    print("""\
=== Cloud Cost Optimization Workflow Simulation ===
Components:
- Cloud Providers (AWS/Azure/GCP)
- VictoriaMetrics (Time Series DB)
- AlertManager → Kafka (Event Streaming)
- Argo Workflows + Admission Controller (Automation)
    """)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSimulation stopped")
