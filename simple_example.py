#!/usr/bin/env python3
"""
Simple Example for llm-prompt-optimizer

A basic demonstration of the package features.
Author: Sherin Joseph Roy
"""

import asyncio
from prompt_optimizer import (
    PromptOptimizer,
    OptimizerConfig,
    ProviderType,
    MetricType
)
from prompt_optimizer.types import (
    PromptVariant,
    ExperimentConfig,
    Experiment,
    TestResult,
    AnalysisReport,
    TestStatus
)


async def simple_demo():
    """Simple demonstration of llm-prompt-optimizer features."""
    
    print("🎯 llm-prompt-optimizer Simple Demo")
    print("=" * 40)
    print("Author: Sherin Joseph Roy")
    print("Package: llm-prompt-optimizer v0.1.1")
    print("=" * 40)
    
    # 1. Create configuration
    print("\n1️⃣ Creating configuration...")
    config = OptimizerConfig(
        database_url="sqlite:///demo.db",
        default_provider=ProviderType.OPENAI,
        api_keys={
            ProviderType.OPENAI: "your-openai-key-here",
        }
    )
    
    # 2. Create prompt variants
    print("\n2️⃣ Creating prompt variants...")
    variants = [
        PromptVariant(
            name="basic",
            template="Help me with: {task}"
        ),
        PromptVariant(
            name="detailed", 
            template="Please provide a detailed explanation for: {task}"
        ),
        PromptVariant(
            name="concise",
            template="Give me a brief answer to: {task}"
        )
    ]
    
    for variant in variants:
        print(f"   ✓ {variant.name}: {variant.template}")
    
    # 3. Create experiment configuration
    print("\n3️⃣ Setting up experiment...")
    experiment_config = ExperimentConfig(
        name="Prompt Style Test",
        description="Compare different prompt styles",
        traffic_split={"basic": 0.33, "detailed": 0.33, "concise": 0.34},
        metrics=[MetricType.QUALITY, MetricType.COST],
        min_sample_size=10,
        max_duration_days=1
    )
    
    # 4. Create experiment
    experiment = Experiment(
        id="demo_experiment_001",
        name=experiment_config.name,
        description=experiment_config.description,
        variants=variants,
        config=experiment_config
    )
    
    print(f"   ✓ Experiment ID: {experiment.id}")
    
    # 5. Simulate test results
    print("\n4️⃣ Running simulated tests...")
    test_inputs = [
        {"task": "Explain machine learning"},
        {"task": "Write a short story"},
        {"task": "Solve a math problem"},
        {"task": "Describe a concept"},
        {"task": "Create a recipe"}
    ]
    
    test_results = []
    for i, test_input in enumerate(test_inputs):
        variant_name = ["basic", "detailed", "concise"][i % 3]
        result = TestResult(
            experiment_id=experiment.id,
            variant_name=variant_name,
            user_id=f"user_{i+1:03d}",
            input_data=test_input,
            response=f"Sample response for {test_input['task']}",
            quality_score=0.7 + (i * 0.05),
            latency_ms=100 + (i * 10),
            cost_usd=0.001 + (i * 0.0001),
            tokens_used=50 + (i * 5)
        )
        test_results.append(result)
        print(f"   ✓ Test {i+1}: {variant_name} - Quality: {result.quality_score:.2f}")
    
    # 6. Analyze results
    print("\n5️⃣ Analyzing results...")
    analysis = AnalysisReport(
        experiment_id=experiment.id,
        status=TestStatus.COMPLETED,
        best_variant="detailed",
        confidence_level=0.95,
        total_samples=len(test_results),
        duration_days=0.1
    )
    
    # 7. Display results
    print("\n" + "="*40)
    print("📊 EXPERIMENT RESULTS")
    print("="*40)
    print(f"Experiment: {analysis.experiment_id}")
    print(f"Status: {analysis.status}")
    print(f"Total Tests: {analysis.total_samples}")
    print(f"Best Variant: {analysis.best_variant}")
    print(f"Confidence: {analysis.confidence_level:.1%}")
    
    print("\n📈 Variant Performance:")
    for variant in variants:
        variant_results = [r for r in test_results if r.variant_name == variant.name]
        if variant_results:
            avg_quality = sum(r.quality_score for r in variant_results) / len(variant_results)
            total_cost = sum(r.cost_usd for r in variant_results)
            print(f"   {variant.name}:")
            print(f"     - Quality: {avg_quality:.3f}")
            print(f"     - Cost: ${total_cost:.4f}")
            print(f"     - Tests: {len(variant_results)}")
    
    print(f"\n🏆 Winner: {analysis.best_variant}")
    
    # 8. CLI and API information
    print("\n" + "="*40)
    print("🛠️  USAGE INFORMATION")
    print("="*40)
    print("CLI Commands:")
    print("  prompt-optimizer --help")
    print("  prompt-optimizer create-experiment --name 'My Test'")
    print("  prompt-optimizer run-test --experiment-id <id>")
    print("  prompt-optimizer analyze --experiment-id <id>")
    
    print("\nAPI Server:")
    print("  uvicorn prompt_optimizer.api.server:app --reload")
    print("  Visit: http://localhost:8000/docs")
    
    print("\n✅ Demo completed successfully!")
    print("="*40)


def main():
    """Main entry point."""
    asyncio.run(simple_demo())


if __name__ == "__main__":
    main() 