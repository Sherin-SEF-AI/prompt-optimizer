"""
FastAPI server for prompt optimization API - RapidAPI Ready.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn
import logging
import asyncio
from datetime import datetime

from ..core.optimizer import PromptOptimizer
from ..types import (
    ProviderType, 
    ExperimentConfig, 
    OptimizationConfig,
    PromptVariant,
    TestResult,
    AnalysisReport,
    OptimizedPrompt,
    Experiment,
    TestStatus,
    OptimizerConfig
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global optimizer instance
optimizer: Optional[PromptOptimizer] = None

def get_optimizer() -> PromptOptimizer:
    """Get the global optimizer instance."""
    if optimizer is None:
        raise HTTPException(status_code=500, detail="Optimizer not initialized")
    return optimizer

# Request/Response Models for API
class CreateExperimentRequest(BaseModel):
    name: str = Field(..., description="Name of the experiment")
    description: Optional[str] = Field(None, description="Description of the experiment")
    variants: List[Dict[str, Any]] = Field(..., description="List of prompt variants")
    config: Dict[str, Any] = Field(..., description="Experiment configuration")

class TestPromptRequest(BaseModel):
    experiment_id: str = Field(..., description="ID of the experiment")
    user_id: str = Field(..., description="User ID for consistent assignment")
    input_data: Dict[str, Any] = Field(..., description="Input data for the prompt")

class OptimizePromptRequest(BaseModel):
    base_prompt: str = Field(..., description="Base prompt to optimize")
    optimization_config: Dict[str, Any] = Field(default_factory=dict, description="Optimization configuration")

class APIResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    message: str = Field(..., description="Response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ErrorResponse(BaseModel):
    success: bool = Field(default=False)
    error: str = Field(..., description="Error message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Factory to create the FastAPI app with a config
def create_app(config: Optional[OptimizerConfig] = None):
    global optimizer
    
    if config is None:
        config = OptimizerConfig()
    
    optimizer = PromptOptimizer(config)
    
    app = FastAPI(
        title="LLM Prompt Optimizer API",
        description="""
        A comprehensive API for systematic A/B testing and optimization of LLM prompts.
        
        ## Features
        - **A/B Testing**: Create and run experiments with multiple prompt variants
        - **Prompt Optimization**: Use genetic algorithms to optimize prompts
        - **Analytics**: Get detailed analysis reports with statistical significance
        - **Multi-Provider Support**: Works with OpenAI, Anthropic, Google, and more
        - **Cost Tracking**: Monitor API costs and token usage
        - **Quality Scoring**: Automated quality assessment of responses
        
        ## Quick Start
        1. Create an experiment with your prompt variants
        2. Start the experiment to begin data collection
        3. Test prompts with your input data
        4. Analyze results to find the best performing variant
        5. Optimize prompts using genetic algorithms
        
        ## Authentication
        Set your API keys in the request headers or use the configuration endpoint.
        """,
        version="0.1.1",
        contact={
            "name": "Sherin Joseph Roy",
            "email": "sherin.joseph2217@gmail.com",
            "url": "https://github.com/Sherin-SEF-AI/prompt-optimizer.git",
        },
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", response_model=APIResponse)
    async def root():
        """Root endpoint with API information."""
        return APIResponse(
            success=True,
            data={
                "api_name": "LLM Prompt Optimizer API",
                "version": "0.1.1",
                "author": "Sherin Joseph Roy",
                "email": "sherin.joseph2217@gmail.com",
                "github": "https://github.com/Sherin-SEF-AI/prompt-optimizer.git",
                "pypi": "https://pypi.org/project/llm-prompt-optimizer/",
                "linkedin": "https://www.linkedin.com/in/sherin-roy-deepmost/",
                "docs": "/docs",
                "endpoints": {
                    "experiments": "/api/v1/experiments",
                    "optimization": "/api/v1/optimize",
                    "analytics": "/api/v1/analytics",
                    "health": "/health"
                }
            },
            message="LLM Prompt Optimizer API is running"
        )

    @app.get("/health", response_model=APIResponse)
    async def health_check():
        """Health check endpoint."""
        return APIResponse(
            success=True,
            data={"status": "healthy", "service": "llm-prompt-optimizer"},
            message="Service is healthy"
        )

    # Experiment Management Endpoints
    @app.post("/api/v1/experiments", response_model=APIResponse)
    async def create_experiment(request: CreateExperimentRequest):
        """Create a new A/B test experiment."""
        try:
            opt = get_optimizer()
            # Convert request to proper types
            variants = [PromptVariant(**variant) for variant in request.variants]
            config = ExperimentConfig(**request.config)
            
            experiment = await opt.create_experiment(
                name=request.name,
                variants=variants,
                config=config
            )
            
            return APIResponse(
                success=True,
                data={
                    "experiment_id": experiment.id,
                    "name": experiment.name,
                    "status": experiment.status,
                    "variants": [{"name": v.name, "template": v.template} for v in experiment.variants],
                    "created_at": experiment.created_at.isoformat()
                },
                message=f"Experiment '{request.name}' created successfully"
            )
        except Exception as e:
            logger.error(f"Error creating experiment: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/api/v1/experiments/{experiment_id}/start", response_model=APIResponse)
    async def start_experiment(experiment_id: str):
        """Start an experiment."""
        try:
            opt = get_optimizer()
            await opt.start_experiment(experiment_id)
            return APIResponse(
                success=True,
                data={"experiment_id": experiment_id, "status": "running"},
                message=f"Experiment {experiment_id} started successfully"
            )
        except Exception as e:
            logger.error(f"Error starting experiment: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/api/v1/experiments/{experiment_id}/stop", response_model=APIResponse)
    async def stop_experiment(experiment_id: str):
        """Stop an experiment."""
        try:
            opt = get_optimizer()
            await opt.stop_experiment(experiment_id)
            return APIResponse(
                success=True,
                data={"experiment_id": experiment_id, "status": "stopped"},
                message=f"Experiment {experiment_id} stopped successfully"
            )
        except Exception as e:
            logger.error(f"Error stopping experiment: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/api/v1/experiments", response_model=APIResponse)
    async def list_experiments():
        """List all experiments."""
        try:
            opt = get_optimizer()
            experiments = await opt.list_experiments()
            return APIResponse(
                success=True,
                data={
                    "experiments": [
                        {
                            "id": exp.id,
                            "name": exp.name,
                            "status": exp.status,
                            "variants_count": len(exp.variants),
                            "created_at": exp.created_at.isoformat(),
                            "started_at": exp.started_at.isoformat() if exp.started_at else None
                        }
                        for exp in experiments
                    ]
                },
                message=f"Found {len(experiments)} experiments"
            )
        except Exception as e:
            logger.error(f"Error listing experiments: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/api/v1/experiments/{experiment_id}", response_model=APIResponse)
    async def get_experiment(experiment_id: str):
        """Get experiment details."""
        try:
            opt = get_optimizer()
            experiments = await opt.list_experiments()
            experiment = next((exp for exp in experiments if exp.id == experiment_id), None)
            
            if not experiment:
                raise HTTPException(status_code=404, detail="Experiment not found")
            
            return APIResponse(
                success=True,
                data={
                    "id": experiment.id,
                    "name": experiment.name,
                    "description": experiment.description,
                    "status": experiment.status,
                    "variants": [
                        {
                            "name": v.name,
                            "template": v.template,
                            "parameters": v.parameters,
                            "version": v.version
                        }
                        for v in experiment.variants
                    ],
                    "config": experiment.config.dict(),
                    "created_at": experiment.created_at.isoformat(),
                    "started_at": experiment.started_at.isoformat() if experiment.started_at else None,
                    "completed_at": experiment.completed_at.isoformat() if experiment.completed_at else None
                },
                message=f"Experiment {experiment_id} details retrieved"
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting experiment: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Testing Endpoints
    @app.post("/api/v1/test", response_model=APIResponse)
    async def test_prompt(request: TestPromptRequest):
        """Test a prompt for a specific experiment."""
        try:
            opt = get_optimizer()
            result = await opt.test_prompt(
                experiment_id=request.experiment_id,
                user_id=request.user_id,
                input_data=request.input_data
            )
            
            return APIResponse(
                success=True,
                data={
                    "experiment_id": result.experiment_id,
                    "variant_name": result.variant_name,
                    "user_id": result.user_id,
                    "response": result.response,
                    "quality_score": result.quality_score,
                    "latency_ms": result.latency_ms,
                    "cost_usd": result.cost_usd,
                    "tokens_used": result.tokens_used,
                    "timestamp": result.timestamp.isoformat()
                },
                message="Prompt test completed successfully"
            )
        except Exception as e:
            logger.error(f"Error testing prompt: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Analytics Endpoints
    @app.get("/api/v1/experiments/{experiment_id}/analyze", response_model=APIResponse)
    async def analyze_experiment(experiment_id: str):
        """Analyze an experiment and get results."""
        try:
            opt = get_optimizer()
            report = await opt.analyze_experiment(experiment_id)
            
            return APIResponse(
                success=True,
                data={
                    "experiment_id": report.experiment_id,
                    "status": report.status,
                    "best_variant": report.best_variant,
                    "confidence_level": report.confidence_level,
                    "total_samples": report.total_samples,
                    "duration_days": report.duration_days,
                    "significance_results": [
                        {
                            "variant_a": result.variant_a,
                            "variant_b": result.variant_b,
                            "is_significant": result.is_significant,
                            "p_value": result.p_value,
                            "effect_size": result.effect_size
                        }
                        for result in report.significance_results
                    ],
                    "metrics_summary": report.metrics_summary,
                    "recommendations": report.recommendations,
                    "created_at": report.created_at.isoformat()
                },
                message=f"Analysis completed for experiment {experiment_id}"
            )
        except Exception as e:
            logger.error(f"Error analyzing experiment: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/api/v1/experiments/{experiment_id}/results", response_model=APIResponse)
    async def get_experiment_results(experiment_id: str):
        """Get all test results for an experiment."""
        try:
            opt = get_optimizer()
            results = await opt.get_experiment_results(experiment_id)
            
            return APIResponse(
                success=True,
                data={
                    "experiment_id": experiment_id,
                    "results": [
                        {
                            "variant_name": result.variant_name,
                            "user_id": result.user_id,
                            "response": result.response,
                            "quality_score": result.quality_score,
                            "latency_ms": result.latency_ms,
                            "cost_usd": result.cost_usd,
                            "tokens_used": result.tokens_used,
                            "timestamp": result.timestamp.isoformat()
                        }
                        for result in results
                    ],
                    "total_results": len(results)
                },
                message=f"Retrieved {len(results)} results for experiment {experiment_id}"
            )
        except Exception as e:
            logger.error(f"Error getting experiment results: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Optimization Endpoints
    @app.post("/api/v1/optimize", response_model=APIResponse)
    async def optimize_prompt(request: OptimizePromptRequest):
        """Optimize a prompt using genetic algorithms."""
        try:
            opt = get_optimizer()
            config = OptimizationConfig(**request.optimization_config)
            
            optimized = await opt.optimize_prompt(
                base_prompt=request.base_prompt,
                optimization_config=config
            )
            
            return APIResponse(
                success=True,
                data={
                    "original_prompt": optimized.original_prompt,
                    "optimized_prompt": optimized.optimized_prompt,
                    "improvement_score": optimized.improvement_score,
                    "metrics_improvement": optimized.metrics_improvement,
                    "optimization_history": optimized.optimization_history,
                    "created_at": optimized.created_at.isoformat()
                },
                message="Prompt optimization completed successfully"
            )
        except Exception as e:
            logger.error(f"Error optimizing prompt: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Export Endpoints
    @app.get("/api/v1/experiments/{experiment_id}/export")
    async def export_results(experiment_id: str, format: str = "csv"):
        """Export experiment results."""
        try:
            if format not in ["csv", "json"]:
                raise HTTPException(status_code=400, detail="Format must be 'csv' or 'json'")
            
            opt = get_optimizer()
            export_data = await opt.export_results(experiment_id, format)
            
            return JSONResponse(
                content={
                    "success": True,
                    "data": export_data,
                    "message": f"Results exported in {format.upper()} format",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        except Exception as e:
            logger.error(f"Error exporting results: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Configuration Endpoints
    @app.get("/api/v1/config", response_model=APIResponse)
    async def get_config():
        """Get current configuration."""
        try:
            opt = get_optimizer()
            return APIResponse(
                success=True,
                data={
                    "database_url": opt.config.database_url,
                    "default_provider": opt.config.default_provider,
                    "max_concurrent_tests": opt.config.max_concurrent_tests,
                    "cache_ttl": opt.config.cache_ttl,
                    "log_level": opt.config.log_level,
                    "providers": list(opt.providers.keys())
                },
                message="Configuration retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error getting config: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    # Error handlers
    @app.exception_handler(404)
    async def not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content=ErrorResponse(
                error="Endpoint not found",
                timestamp=datetime.utcnow()
            ).dict()
        )

    @app.exception_handler(500)
    async def internal_error_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="Internal server error",
                timestamp=datetime.utcnow()
            ).dict()
        )

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 