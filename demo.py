import random
import asyncio

# Simulated cloud providers
cloud_providers = ['AWS', 'Azure', 'GCP']
services = {'AWS': ['EC2', 'S3', 'Lambda'], 'Azure': ['VM', 'Storage', 'Functions'], 'GCP': ['Compute', 'Storage', 'BigQuery']}

# Baseline costs for simulation
baseline_costs = {
    'AWS': {'EC2': 300, 'S3': 150, 'Lambda': 100},
    'Azure': {'VM': 250, 'Storage': 120, 'Functions': 80},
    'GCP': {'Compute': 280, 'Storage': 130, 'BigQuery': 200}
}

# Simulated data stores
metrics_store = {}
optimization_results = []

async def fluentbit_collect_logs():
    """Simulate Fluent Bit collecting logs from cloud providers"""
    for _ in range(3):  # limited iterations for demo
        for provider in cloud_providers:
            for service in services[provider]:
                # Add some randomness to make some costs spike above baseline
                cost_factor = random.uniform(0.8, 1.8) if random.random() > 0.7 else random.uniform(0.8, 1.1)
                cost = baseline_costs[provider][service] * cost_factor
                
                # Store in metrics database
                if provider not in metrics_store:
                    metrics_store[provider] = {}
                metrics_store[provider][service] = cost
                
                print(f"📊 [Fluent Bit] Collecting logs from {provider} {service}")
                print(f"📊 [VictoriaMetrics] Stored {provider} {service} cost: ${cost:.2f}")
        
        # Allow time for AlertManager to check metrics
        await asyncio.sleep(1)

async def alertmanager_check_metrics():
    """Simulate AlertManager checking metrics and detecting anomalies"""
    # Wait for initial data collection
    await asyncio.sleep(1)
    
    for _ in range(3):  # limited iterations for demo
        for provider in metrics_store:
            for service, cost in metrics_store[provider].items():
                baseline = baseline_costs[provider][service]
                deviation = ((cost - baseline) / baseline) * 100
                
                # Alert if cost exceeds threshold (20% above baseline)
                if deviation > 20:
                    print(f"🚨 [AlertManager] Cost anomaly detected! {provider} {service} ${cost:.2f} ({deviation:.1f}% above baseline)")
                    
                    # Create event
                    event = {
                        'provider': provider,
                        'service': service,
                        'current_cost': cost,
                        'baseline_cost': baseline,
                        'deviation_percentage': deviation
                    }
                    
                    # Send to Kafka
                    await kafka_produce_event(event)
                    
                    # Create incident in Zenduty for critical anomalies
                    if deviation > 50:
                        print(f"🔔 [Zenduty] Created incident for {provider} {service} cost spike ({deviation:.1f}%)")
        
        await asyncio.sleep(1)

async def kafka_produce_event(event):
    """Simulate Kafka producing an event"""
    print(f"🔁 [Kafka] Producing event: {{provider: \"{event['provider']}\", service: \"{event['service']}\", deviation: {event['deviation_percentage']:.1f}%}}")
    
    # Pass event to Argo Workflows
    await argo_consume_event(event)

async def argo_consume_event(event):
    """Simulate Argo Workflows consuming event and triggering optimization"""
    print(f"⚙️ [Argo Workflows] Starting {event['service'].lower()}-optimization workflow")
    
    # Get credentials from Vault
    print(f"🔑 [HashiCorp Vault] Retrieved {event['provider']} credentials")
    
    # Check policy with AdmissionController
    approved = admission_controller_policy_check(event)
    
    if approved:
        print(f"🔒 [AdmissionController] Policy validation passed")
        
        # Simulate optimization (20% cost reduction)
        optimized_cost = event['current_cost'] * 0.8
        print(f"📉 [Argo Workflows] Rightsizing complete: ${event['current_cost']:.2f} → ${optimized_cost:.2f} (20% reduction)")
        
        # Store optimization result in PostgreSQL
        store_result_in_postgres(event, optimized_cost)
    else:
        print(f"❌ [AdmissionController] Policy validation failed")

def admission_controller_policy_check(event):
    """Simulate policy validation logic"""
    # For simplicity, approve all events with deviation less than 100%
    # In a real system, this would check against organizational policies
    return event['deviation_percentage'] < 100

def store_result_in_postgres(event, optimized_cost):
    """Simulate storing results in PostgreSQL"""
    result = {
        'provider': event['provider'],
        'service': event['service'],
        'before_cost': event['current_cost'],
        'after_cost': optimized_cost,
        'savings': event['current_cost'] - optimized_cost
    }
    optimization_results.append(result)
    print(f"💾 [PostgreSQL] Stored optimization result for {event['provider']} {event['service']}")

async def main():
    """Main function to coordinate all components"""
    print("🚀 Starting Cloud Cost Tracking System Simulation")
    print("================================================")
    
    # Run collection and alerting concurrently
    collection_task = asyncio.create_task(fluentbit_collect_logs())
    alerting_task = asyncio.create_task(alertmanager_check_metrics())
    
    # Wait for all tasks to complete
    await asyncio.gather(
        collection_task,
        alerting_task
    )
    
    # Print summary of optimizations
    print("\n📊 Optimization Results Summary")
    print("==============================")
    total_savings = 0
    for result in optimization_results:
        savings = result['before_cost'] - result['after_cost']
        total_savings += savings
        print(f"• {result['provider']} {result['service']}: ${savings:.2f} saved")
    
    print(f"\nTotal estimated monthly savings: ${total_savings:.2f}")
    
    # Visualize in Grafana (simulated)
    print("\n📈 [Grafana] Updated cost optimization dashboard with latest results")

# Run the async main function
asyncio.run(main())
