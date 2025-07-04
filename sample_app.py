#!/usr/bin/env python3
"""
Sample Application for llm-prompt-optimizer

This demonstrates:
- A/B testing with multiple prompt variants
- Prompt optimization using genetic algorithms
- Performance analytics and cost tracking
- Quality scoring and statistical analysis
- CLI integration and API usage

Author: Sherin Joseph Roy
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Any

# Import the llm-prompt-optimizer package
from prompt_optimizer import (
    PromptOptimizer,
    OptimizerConfig,
    ExperimentConfig,
    ProviderType,
    MetricType,
    OptimizationConfig,
    QualityScorer,
    CostTracker,
    PerformanceAnalyzer,
    TestResult,
    AnalysisReport,
    TestStatus,
    Experiment
)
from prompt_optimizer.types import (
    PromptVariant,
    Experiment
)


class SamplePromptOptimizerApp:
    """Sample application demonstrating llm-prompt-optimizer features."""
    
    def __init__(self):
        """Initialize the sample application."""
        self.config = self._create_config()
        self.optimizer = PromptOptimizer(self.config)
        self.quality_scorer = QualityScorer()
        self.cost_tracker = CostTracker()
        self.performance_analyzer = PerformanceAnalyzer()
        
        # Sample test data
        self.test_inputs = [
            {"task": "Explain machine learning in simple terms", "user_id": "user_001"},
            {"task": "Write a short story about a robot", "user_id": "user_002"},
            {"task": "Summarize the benefits of renewable energy", "user_id": "user_003"},
            {"task": "Create a recipe for chocolate chip cookies", "user_id": "user_004"},
            {"task": "Explain quantum computing basics", "user_id": "user_005"},
        ]
        
        # Sample prompt variants for A/B testing
        self.prompt_variants = [
            PromptVariant(
                name="variant_a",
                template="You are a helpful assistant. Please help with: {task}",
                metadata={"description": "Basic helpful assistant prompt"}
            ),
            PromptVariant(
                name="variant_b", 
                template="You are an expert in your field. Please provide a detailed response to: {task}",
                metadata={"description": "Expert-focused prompt"}
            ),
            PromptVariant(
                name="variant_c",
                template="I need your assistance with the following task. Please be concise and accurate: {task}",
                metadata={"description": "Concise and accurate prompt"}
            ),
            PromptVariant(
                name="variant_d",
                template="As a knowledgeable AI assistant, I'd be happy to help you with: {task}. Please provide a comprehensive answer.",
                metadata={"description": "Comprehensive answer prompt"}
            )
        ]
    
    def _create_config(self) -> OptimizerConfig:
        """Create configuration for the optimizer."""
        return OptimizerConfig(
            database_url="sqlite:///sample_optimizer.db",
            default_provider=ProviderType.OPENAI,
            api_keys={
                ProviderType.OPENAI: os.getenv("OPENAI_API_KEY", "your-openai-key-here"),
                ProviderType.ANTHROPIC: os.getenv("ANTHROPIC_API_KEY", "your-anthropic-key-here"),
            },
            cache_ttl=3600,
            log_level="INFO"
        )
    
    async def run_ab_test_experiment(self) -> str:
        """Run a complete A/B test experiment."""
        print("🚀 Starting A/B Test Experiment...")
        
        # Create experiment configuration
        experiment_config = ExperimentConfig(
            name="Prompt Style Comparison",
            description="Compare different prompt styles for better user engagement",
            traffic_split={
                "variant_a": 0.25,
                "variant_b": 0.25,
                "variant_c": 0.25,
                "variant_d": 0.25
            },
            metrics=[MetricType.QUALITY, MetricType.COST, MetricType.LATENCY],
            min_sample_size=20,
            max_duration_days=1,
            significance_level=0.05
        )
        
        # Create experiment object
        experiment = Experiment(
            id="sample_experiment_001",
            name=experiment_config.name,
            description=experiment_config.description,
            variants=self.prompt_variants,
            config=experiment_config
        )
        
        print(f"✅ Experiment created with ID: {experiment.id}")
        
        # Simulate test results
        print("📊 Running tests with sample data...")
        test_results = []
        for i, test_input in enumerate(self.test_inputs):
            # Simulate a test result
            result = TestResult(
                experiment_id=experiment.id,
                variant_name=f"variant_{chr(97 + (i % 4))}",  # a, b, c, d
                user_id=test_input["user_id"],
                input_data=test_input,
                response=f"Sample response for {test_input['task']}",
                quality_score=0.7 + (i * 0.05),  # Simulate varying quality
                latency_ms=100 + (i * 10),
                cost_usd=0.001 + (i * 0.0001),
                tokens_used=50 + (i * 5)
            )
            test_results.append(result)
            print(f"  Test {i+1}: {result.variant_name} - Quality: {result.quality_score:.2f}")
        
        # Simulate analysis results
        print("📈 Analyzing experiment results...")
        analysis = AnalysisReport(
            experiment_id=experiment.id,
            status=TestStatus.COMPLETED,
            best_variant="variant_b",
            confidence_level=0.95,
            total_samples=len(test_results),
            duration_days=0.1
        )
        
        # Print analysis results
        print("\n" + "="*50)
        print("EXPERIMENT ANALYSIS RESULTS")
        print("="*50)
        print(f"Experiment ID: {analysis.experiment_id}")
        print(f"Status: {analysis.status}")
        print(f"Total Samples: {analysis.total_samples}")
        print(f"Duration: {analysis.duration_days:.1f} days")
        print(f"Best Variant: {analysis.best_variant}")
        print(f"Confidence Level: {analysis.confidence_level:.1%}")
        
        print("\n📊 Variant Performance Summary:")
        for variant in self.prompt_variants:
            variant_results = [r for r in test_results if r.variant_name == variant.name]
            if variant_results:
                avg_quality = sum(r.quality_score for r in variant_results) / len(variant_results)
                total_cost = sum(r.cost_usd for r in variant_results)
                avg_latency = sum(r.latency_ms for r in variant_results) / len(variant_results)
                print(f"  {variant.name}:")
                print(f"    - Quality Score: {avg_quality:.3f}")
                print(f"    - Cost: ${total_cost:.4f}")
                print(f"    - Latency: {avg_latency:.2f}ms")
                print(f"    - Sample Size: {len(variant_results)}")
        
        print(f"\n🏆 Winner: {analysis.best_variant}")
        print("✅ Experiment completed successfully")
        
        return experiment.id
    
    async def optimize_prompt(self, base_prompt: str) -> Dict[str, Any]:
        """Optimize a prompt using genetic algorithms."""
        print(f"\n🧬 Optimizing prompt: {base_prompt[:50]}...")
        
        # Create optimization configuration
        optimization_config = OptimizationConfig(
            target_metrics=[MetricType.QUALITY, MetricType.COST],
            max_iterations=10,
            population_size=8,
            mutation_rate=0.15,
            crossover_rate=0.8,
            fitness_threshold=0.85
        )
        
        # Run optimization
        optimized_result = await self.optimizer.optimize_prompt(
            base_prompt=base_prompt,
            optimization_config=optimization_config
        )
        
        print("\n" + "="*50)
        print("PROMPT OPTIMIZATION RESULTS")
        print("="*50)
        print(f"Original Prompt: {optimized_result.original_prompt}")
        print(f"Optimized Prompt: {optimized_result.optimized_prompt}")
        print(f"Improvement Score: {optimized_result.improvement_score:.3f}")
        
        print("\n📈 Metrics Improvement:")
        for metric, improvement in optimized_result.metrics_improvement.items():
            print(f"  {metric}: {improvement:+.1%}")
        
        return optimized_result.dict()
    
    async def analyze_performance(self, experiment_id: str):
        """Analyze performance metrics for an experiment."""
        print(f"\n📊 Analyzing performance for experiment {experiment_id}...")
        
        # Simulate performance analysis
        print("\n" + "="*50)
        print("PERFORMANCE ANALYSIS")
        print("="*50)
        print(f"Total Requests: 25")
        print(f"Average Response Time: 150.5ms")
        print(f"Success Rate: 100.0%")
        print(f"Total Cost: $0.0050")
        
        print(f"\n🔤 Token Efficiency:")
        print(f"  Average Tokens per Request: 55.2")
        print(f"  Efficiency Score: 0.847")
        
        # Quality analysis
        print(f"\n⭐ Quality Analysis:")
        print(f"  Average Quality Score: 0.725")
        print(f"  Quality Range: 0.700 - 0.950")
    
    async def demonstrate_cli_integration(self):
        """Demonstrate CLI integration."""
        print("\n🖥️  CLI Integration Demo:")
        print("You can also use the command-line interface:")
        print("  prompt-optimizer --help")
        print("  prompt-optimizer create-experiment --name 'My Test' --variants 2")
        print("  prompt-optimizer run-test --experiment-id <id> --input 'test data'")
        print("  prompt-optimizer analyze --experiment-id <id>")
        print("  prompt-optimizer optimize --prompt 'Your prompt here'")
    
    async def demonstrate_api_usage(self):
        """Demonstrate API usage."""
        print("\n🌐 API Usage Demo:")
        print("Start the API server with:")
        print("  uvicorn prompt_optimizer.api.server:app --reload")
        print("\nThen access:")
        print("  - API Documentation: http://localhost:8000/docs")
        print("  - Health Check: http://localhost:8000/health")
        print("  - Root Info: http://localhost:8000/")
    
    async def run_complete_demo(self):
        """Run the complete demonstration."""
        print("🎯 llm-prompt-optimizer Sample Application")
        print("=" * 50)
        print("Author: Sherin Joseph Roy")
        print("Package: llm-prompt-optimizer")
        print("Version: 0.1.1")
        print("=" * 50)
        
        try:
            # Run A/B test experiment
            experiment_id = await self.run_ab_test_experiment()
            
            # Optimize a sample prompt
            base_prompt = "You are a helpful assistant. Please help with: {task}"
            optimization_result = await self.optimize_prompt(base_prompt)
            
            # Analyze performance
            await self.analyze_performance(experiment_id)
            
            # Demonstrate CLI and API usage
            await self.demonstrate_cli_integration()
            await self.demonstrate_api_usage()
            
            print("\n" + "="*50)
            print("✅ Demo completed successfully!")
            print("="*50)
            
        except Exception as e:
            print(f"\n❌ Error during demo: {e}")
            print("Make sure you have valid API keys set in environment variables:")
            print("  export OPENAI_API_KEY='your-key-here'")
            print("  export ANTHROPIC_API_KEY='your-key-here'")
        
        finally:
            # Cleanup
            await self.optimizer.cleanup()


def main():
    """Main entry point for the sample application."""
    app = SamplePromptOptimizerApp()
    
    # Run the async demo
    asyncio.run(app.run_complete_demo())


if __name__ == "__main__":
    main() 