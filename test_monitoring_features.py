#!/usr/bin/env python3
"""
Test script for monitoring features to ensure they work properly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from prompt_optimizer.monitoring import RealTimeDashboard
from prompt_optimizer.monitoring.real_time_dashboard import MetricType, AlertLevel
from datetime import datetime, timedelta


async def test_dashboard_initialization():
    """Test dashboard initialization."""
    print("📈 Testing Dashboard Initialization...")
    
    try:
        dashboard = RealTimeDashboard()
        print("    ✅ PASS - Dashboard initialized successfully")
        return True
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


async def test_metric_management():
    """Test metric management functionality."""
    print("\n📊 Testing Metric Management...")
    
    dashboard = RealTimeDashboard()
    
    try:
        # Test adding metrics
        dashboard.add_metric_point(
            metric_name="quality_score",
            metric_type=MetricType.QUALITY_SCORE,
            value=0.85,
            metadata={"experiment_id": "test_exp", "variant": "control"}
        )
        
        dashboard.add_metric_point(
            metric_name="latency_ms",
            metric_type=MetricType.LATENCY,
            value=1200,
            metadata={"experiment_id": "test_exp", "variant": "control"}
        )
        
        dashboard.add_metric_point(
            metric_name="cost_usd",
            metric_type=MetricType.COST,
            value=0.05,
            metadata={"experiment_id": "test_exp", "variant": "control"}
        )
        
        # Verify metrics were added
        dashboard_data = dashboard.get_dashboard_data()
        assert len(dashboard_data['metrics']) == 3
        
        print("    ✅ PASS - Metrics added successfully")
        print(f"    Total metrics: {len(dashboard_data['metrics'])}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


async def test_experiment_status():
    """Test experiment status management."""
    print("\n🧪 Testing Experiment Status Management...")
    
    dashboard = RealTimeDashboard()
    
    try:
        # Update experiment status
        dashboard.update_experiment_status("test_exp", {
            'name': 'Test Experiment',
            'status': 'running',
            'total_tests': 100,
            'successful_tests': 95,
            'failed_tests': 5,
            'current_traffic': {'control': 50, 'variant': 50},
            'best_variant': 'variant',
            'confidence_level': 0.85
        })
        
        # Verify status was updated
        dashboard_data = dashboard.get_dashboard_data()
        assert len(dashboard_data['experiments']) == 1
        
        experiment = dashboard_data['experiments'][0]
        assert experiment['experiment_id'] == 'test_exp'
        assert experiment['name'] == 'Test Experiment'
        assert experiment['status'] == 'running'
        
        print("    ✅ PASS - Experiment status updated successfully")
        print(f"    Experiment: {experiment['name']} ({experiment['status']})")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


async def test_alert_system():
    """Test alert system functionality."""
    print("\n🚨 Testing Alert System...")
    
    dashboard = RealTimeDashboard()
    
    try:
        # Add metrics that should trigger alerts
        dashboard.add_metric_point(
            metric_name="quality_score_low",
            metric_type=MetricType.QUALITY_SCORE,
            value=0.2,  # Low quality should trigger alert
            metadata={"experiment_id": "test_exp"}
        )
        
        dashboard.add_metric_point(
            metric_name="latency_high",
            metric_type=MetricType.LATENCY,
            value=15000,  # High latency should trigger alert
            metadata={"experiment_id": "test_exp"}
        )
        
        dashboard.add_metric_point(
            metric_name="cost_high",
            metric_type=MetricType.COST,
            value=150.0,  # High cost should trigger alert
            metadata={"experiment_id": "test_exp"}
        )
        
        # Check for alerts
        dashboard_data = dashboard.get_dashboard_data()
        alerts = dashboard_data['alerts']
        
        assert len(alerts) >= 3  # Should have at least 3 alerts
        
        print("    ✅ PASS - Alert system working")
        print(f"    Active alerts: {len(alerts)}")
        for alert in alerts[:3]:  # Show first 3 alerts
            print(f"    - {alert['metric_name']}: {alert['alert_level']}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


async def test_system_health():
    """Test system health monitoring."""
    print("\n💚 Testing System Health Monitoring...")
    
    dashboard = RealTimeDashboard()
    
    try:
        # Add some metrics to calculate health
        for i in range(5):
            dashboard.add_metric_point(
                metric_name=f"test_metric_{i}",
                metric_type=MetricType.QUALITY_SCORE,
                value=0.8 + (i * 0.02),
                metadata={"experiment_id": "test_exp"}
            )
        
        # Get system health
        dashboard_data = dashboard.get_dashboard_data()
        health = dashboard_data['system_health']
        
        assert 'overall_health' in health
        assert 'total_metrics' in health
        assert 'active_experiments' in health
        assert 0 <= health['overall_health'] <= 100
        
        print("    ✅ PASS - System health monitoring working")
        print(f"    Overall health: {health['overall_health']:.1f}%")
        print(f"    Total metrics: {health['total_metrics']}")
        print(f"    Active experiments: {health['active_experiments']}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


async def test_metric_history():
    """Test metric history functionality."""
    print("\n📜 Testing Metric History...")
    
    dashboard = RealTimeDashboard()
    
    try:
        # Add metrics over time
        for i in range(10):
            dashboard.add_metric_point(
                metric_name="historical_metric",
                metric_type=MetricType.QUALITY_SCORE,
                value=0.7 + (i * 0.02),
                metadata={"experiment_id": "test_exp"}
            )
        
        # Get metric history
        history = dashboard.get_metric_history("historical_metric", hours=24)
        
        assert len(history) == 10
        assert all(hasattr(point, 'timestamp') for point in history)
        assert all(hasattr(point, 'value') for point in history)
        
        print("    ✅ PASS - Metric history working")
        print(f"    History points: {len(history)}")
        print(f"    Value range: {min(p.value for p in history):.2f} - {max(p.value for p in history):.2f}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


async def test_experiment_metrics():
    """Test experiment-specific metrics."""
    print("\n🔬 Testing Experiment Metrics...")
    
    dashboard = RealTimeDashboard()
    
    try:
        # Add metrics for specific experiment
        dashboard.add_metric_point(
            metric_name="exp_quality",
            metric_type=MetricType.QUALITY_SCORE,
            value=0.85,
            metadata={"experiment_id": "exp_123", "variant": "control"}
        )
        
        dashboard.add_metric_point(
            metric_name="exp_latency",
            metric_type=MetricType.LATENCY,
            value=1000,
            metadata={"experiment_id": "exp_123", "variant": "control"}
        )
        
        # Get experiment metrics
        exp_metrics = dashboard.get_experiment_metrics("exp_123")
        
        assert len(exp_metrics) == 2
        assert "exp_quality" in exp_metrics
        assert "exp_latency" in exp_metrics
        
        print("    ✅ PASS - Experiment metrics working")
        print(f"    Experiment metrics: {len(exp_metrics)}")
        for metric_name, metric_data in exp_metrics.items():
            print(f"    - {metric_name}: {metric_data['current_value']}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


async def test_dashboard_lifecycle():
    """Test dashboard start/stop lifecycle."""
    print("\n🔄 Testing Dashboard Lifecycle...")
    
    dashboard = RealTimeDashboard()
    
    try:
        # Start dashboard
        await dashboard.start()
        assert dashboard.running == True
        print("    ✅ PASS - Dashboard started successfully")
        
        # Add some metrics while running
        dashboard.add_metric_point(
            metric_name="lifecycle_test",
            metric_type=MetricType.QUALITY_SCORE,
            value=0.9,
            metadata={"test": True}
        )
        
        # Stop dashboard
        await dashboard.stop()
        assert dashboard.running == False
        print("    ✅ PASS - Dashboard stopped successfully")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


async def test_subscription_system():
    """Test subscription system for real-time updates."""
    print("\n📡 Testing Subscription System...")
    
    dashboard = RealTimeDashboard()
    
    try:
        # Test callback function
        updates_received = []
        
        def test_callback(data):
            updates_received.append(data)
        
        # Subscribe to updates
        dashboard.subscribe(test_callback)
        assert len(dashboard.subscribers) == 1
        
        # Add metric to trigger update
        dashboard.add_metric_point(
            metric_name="subscription_test",
            metric_type=MetricType.QUALITY_SCORE,
            value=0.8,
            metadata={"test": True}
        )
        
        # Unsubscribe
        dashboard.unsubscribe(test_callback)
        assert len(dashboard.subscribers) == 0
        
        print("    ✅ PASS - Subscription system working")
        print(f"    Subscribers: {len(dashboard.subscribers)}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


async def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n⚠️ Testing Edge Cases...")
    
    dashboard = RealTimeDashboard()
    
    try:
        # Test with empty metric name
        dashboard.add_metric_point(
            metric_name="",
            metric_type=MetricType.QUALITY_SCORE,
            value=0.5,
            metadata={}
        )
        print("    ✅ PASS - Empty metric name handling")
        
        # Test with invalid metric type
        dashboard.add_metric_point(
            metric_name="test_metric",
            metric_type="invalid_type",
            value=0.5,
            metadata={}
        )
        print("    ✅ PASS - Invalid metric type handling")
        
        # Test with None values
        dashboard.add_metric_point(
            metric_name="none_test",
            metric_type=MetricType.QUALITY_SCORE,
            value=0.5,
            metadata=None
        )
        print("    ✅ PASS - None metadata handling")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


async def main():
    """Run all monitoring feature tests."""
    print("📈 Monitoring Features Test Suite")
    print("=" * 50)
    
    tests = [
        ("Initialization", test_dashboard_initialization),
        ("Metric Management", test_metric_management),
        ("Experiment Status", test_experiment_status),
        ("Alert System", test_alert_system),
        ("System Health", test_system_health),
        ("Metric History", test_metric_history),
        ("Experiment Metrics", test_experiment_metrics),
        ("Dashboard Lifecycle", test_dashboard_lifecycle),
        ("Subscription System", test_subscription_system),
        ("Edge Cases", test_edge_cases),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = await test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All monitoring features are working properly!")
        return True
    else:
        print("⚠️ Some monitoring features need attention.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1) 