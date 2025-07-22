#!/usr/bin/env python3
"""
Test script for analytics features to ensure they work properly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prompt_optimizer.analytics.advanced import PredictiveAnalytics
from prompt_optimizer.analytics.advanced.predictive_analytics import PredictionResult
from datetime import datetime, timedelta
import numpy as np


def test_predictive_analytics_initialization():
    """Test predictive analytics initialization."""
    print("📊 Testing Predictive Analytics Initialization...")
    
    try:
        analytics = PredictiveAnalytics()
        print("    ✅ PASS - Analytics initialized successfully")
        return True
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


def test_quality_prediction():
    """Test quality score prediction."""
    print("\n🎯 Testing Quality Score Prediction...")
    
    analytics = PredictiveAnalytics()
    
    # Sample historical data
    historical_data = [
        {
            'prompt_length': 50,
            'word_count': 10,
            'sentence_count': 2,
            'avg_word_length': 5.0,
            'complexity_score': 0.3,
            'specificity_score': 0.7,
            'clarity_score': 0.8,
            'tone_score': 0.6,
            'context_relevance': 0.9,
            'quality_score': 0.85
        },
        {
            'prompt_length': 100,
            'word_count': 20,
            'sentence_count': 3,
            'avg_word_length': 4.5,
            'complexity_score': 0.5,
            'specificity_score': 0.8,
            'clarity_score': 0.7,
            'tone_score': 0.8,
            'context_relevance': 0.8,
            'quality_score': 0.78
        },
        {
            'prompt_length': 75,
            'word_count': 15,
            'sentence_count': 2,
            'avg_word_length': 4.8,
            'complexity_score': 0.4,
            'specificity_score': 0.75,
            'clarity_score': 0.75,
            'tone_score': 0.7,
            'context_relevance': 0.85,
            'quality_score': 0.82
        }
    ]
    
    # Test prompt features
    test_features = {
        'prompt_length': 80,
        'word_count': 16,
        'sentence_count': 3,
        'avg_word_length': 4.7,
        'complexity_score': 0.45,
        'specificity_score': 0.78,
        'clarity_score': 0.76,
        'tone_score': 0.72,
        'context_relevance': 0.87
    }
    
    try:
        prediction = analytics.predict_quality_score(test_features, historical_data)
        
        # Validate prediction result
        assert isinstance(prediction, PredictionResult)
        assert 0.0 <= prediction.predicted_value <= 1.0
        assert len(prediction.confidence_interval) == 2
        assert prediction.confidence_interval[0] <= prediction.confidence_interval[1]
        assert 0.0 <= prediction.confidence_level <= 1.0
        assert 0.0 <= prediction.model_accuracy <= 1.0
        assert isinstance(prediction.features_importance, dict)
        assert prediction.prediction_horizon == "immediate"
        
        print(f"    ✅ PASS - Quality prediction: {prediction.predicted_value:.3f}")
        print(f"    Confidence interval: {prediction.confidence_interval}")
        print(f"    Model accuracy: {prediction.model_accuracy:.3f}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


def test_cost_prediction():
    """Test cost trend prediction."""
    print("\n💰 Testing Cost Trend Prediction...")
    
    analytics = PredictiveAnalytics()
    
    # Generate historical cost data
    historical_costs = []
    base_cost = 0.05
    for i in range(30, 0, -1):
        historical_costs.append({
            'timestamp': datetime.now() - timedelta(days=i),
            'cost_usd': base_cost + (i * 0.001) + np.random.normal(0, 0.002)
        })
    
    try:
        predictions = analytics.predict_cost_trend("test_prompt", historical_costs, forecast_days=7)
        
        # Validate predictions
        assert len(predictions) == 7
        assert all(isinstance(pred, PredictionResult) for pred in predictions)
        assert all(0.0 <= pred.predicted_value for pred in predictions)
        assert all(len(pred.confidence_interval) == 2 for pred in predictions)
        
        print(f"    ✅ PASS - Generated {len(predictions)} cost predictions")
        for i, pred in enumerate(predictions[:3]):  # Show first 3
            print(f"    Day {i+1}: ${pred.predicted_value:.4f} (CI: ${pred.confidence_interval[0]:.4f}-${pred.confidence_interval[1]:.4f})")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


def test_conversion_prediction():
    """Test conversion rate prediction."""
    print("\n📈 Testing Conversion Rate Prediction...")
    
    analytics = PredictiveAnalytics()
    
    # Sample historical data for conversion prediction
    historical_data = [
        {
            'quality_score': 0.8,
            'response_time': 1000,
            'cost_usd': 0.05,
            'user_satisfaction': 0.9,
            'click_through_rate': 0.15,
            'engagement_score': 0.85,
            'relevance_score': 0.9,
            'conversion_rate': 0.12
        },
        {
            'quality_score': 0.75,
            'response_time': 800,
            'cost_usd': 0.04,
            'user_satisfaction': 0.85,
            'click_through_rate': 0.12,
            'engagement_score': 0.8,
            'relevance_score': 0.85,
            'conversion_rate': 0.10
        },
        {
            'quality_score': 0.85,
            'response_time': 1200,
            'cost_usd': 0.06,
            'user_satisfaction': 0.95,
            'click_through_rate': 0.18,
            'engagement_score': 0.9,
            'relevance_score': 0.95,
            'conversion_rate': 0.15
        }
    ]
    
    # Test variants
    variants = [
        {
            'name': 'variant_a',
            'quality_score': 0.82,
            'response_time': 1100,
            'cost_usd': 0.055,
            'user_satisfaction': 0.88,
            'click_through_rate': 0.16,
            'engagement_score': 0.87,
            'relevance_score': 0.92
        },
        {
            'name': 'variant_b',
            'quality_score': 0.78,
            'response_time': 900,
            'cost_usd': 0.045,
            'user_satisfaction': 0.82,
            'click_through_rate': 0.13,
            'engagement_score': 0.83,
            'relevance_score': 0.88
        }
    ]
    
    try:
        predictions = analytics.predict_conversion_rate(variants, historical_data)
        
        # Validate predictions
        assert len(predictions) == len(variants)
        assert all(isinstance(pred, PredictionResult) for pred in predictions.values())
        assert all(0.0 <= pred.predicted_value <= 1.0 for pred in predictions.values())
        
        print(f"    ✅ PASS - Generated {len(predictions)} conversion predictions")
        for variant, pred in predictions.items():
            print(f"    {variant}: {pred.predicted_value:.3f} conversion rate")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


def test_optimal_traffic_split():
    """Test optimal traffic split prediction."""
    print("\n🎲 Testing Optimal Traffic Split...")
    
    analytics = PredictiveAnalytics()
    
    # Sample variants
    variants = [
        {'name': 'control', 'quality_score': 0.8, 'cost_usd': 0.05},
        {'name': 'variant_a', 'quality_score': 0.85, 'cost_usd': 0.06},
        {'name': 'variant_b', 'quality_score': 0.82, 'cost_usd': 0.055}
    ]
    
    # Sample historical data
    historical_data = [
        {'quality_score': 0.8, 'conversion_rate': 0.1},
        {'quality_score': 0.85, 'conversion_rate': 0.12},
        {'quality_score': 0.82, 'conversion_rate': 0.11}
    ]
    
    try:
        optimal_split = analytics.predict_optimal_traffic_split(variants, historical_data, total_traffic=1000)
        
        # Validate traffic split
        assert len(optimal_split) == len(variants)
        assert all(0.0 <= split <= 1.0 for split in optimal_split.values())
        assert abs(sum(optimal_split.values()) - 1.0) < 0.01  # Should sum to 1.0
        
        print(f"    ✅ PASS - Generated optimal traffic split")
        for variant, split in optimal_split.items():
            print(f"    {variant}: {split:.1%}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ERROR - {e}")
        return False


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n⚠️ Testing Edge Cases...")
    
    analytics = PredictiveAnalytics()
    
    # Test with empty historical data
    try:
        result = analytics.predict_quality_score({}, [])
        assert result.predicted_value == 0.5  # Default value
        print("    ✅ PASS - Empty data handling")
    except Exception as e:
        print(f"    ❌ ERROR - Empty data handling: {e}")
        return False
    
    # Test with insufficient data
    try:
        result = analytics.predict_quality_score({'prompt_length': 50}, [{'quality_score': 0.8}])
        assert result.predicted_value == 0.5  # Default value
        print("    ✅ PASS - Insufficient data handling")
    except Exception as e:
        print(f"    ❌ ERROR - Insufficient data handling: {e}")
        return False
    
    # Test with invalid features
    try:
        result = analytics.predict_quality_score(None, [{'quality_score': 0.8}])
        print("    ✅ PASS - Invalid features handling")
    except Exception as e:
        print(f"    ❌ ERROR - Invalid features handling: {e}")
        return False
    
    return True


def main():
    """Run all analytics feature tests."""
    print("📊 Analytics Features Test Suite")
    print("=" * 50)
    
    tests = [
        ("Initialization", test_predictive_analytics_initialization),
        ("Quality Prediction", test_quality_prediction),
        ("Cost Prediction", test_cost_prediction),
        ("Conversion Prediction", test_conversion_prediction),
        ("Traffic Split", test_optimal_traffic_split),
        ("Edge Cases", test_edge_cases),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
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
        print("🎉 All analytics features are working properly!")
        return True
    else:
        print("⚠️ Some analytics features need attention.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 