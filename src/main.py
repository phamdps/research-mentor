"""
Main entry point for the Research Assistant application.
Can be run as a CLI tool or import the API app.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from loguru import logger
from config.settings import settings
from config.logging_config import setup_logging
from src.core.models import ResearchQuery
from src.workflows.research_workflow import ResearchWorkflow


async def run_cli():
    """Run the research assistant in CLI mode."""
    setup_logging(
        log_level=settings.LOG_LEVEL,
        log_file=settings.LOGS_DIR / "cli.log",
        log_format="text"
    )
    
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"LLM Provider: {settings.LLM_PROVIDER} ({settings.LLM_MODEL_NAME})")
    
    # Get research topic from command line or use default
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter research topic: ")
    
    if not topic.strip():
        logger.error("No topic provided")
        return
    
    # Create research query
    query = ResearchQuery(
        topic=topic,
        description=f"Research analysis of: {topic}",
        keywords=topic.split()[:5],
        max_sources=10
    )
    
    # Initialize workflow
    workflow = ResearchWorkflow()
    
    logger.info(f"Starting research on: {topic}")
    print(f"\n{'='*60}")
    print(f"Researching: {topic}")
    print(f"{'='*60}\n")
    
    try:
        # Execute research
        result = await workflow.execute(query)
        
        # Display results
        print(f"\n{'='*60}")
        print(f"Research Complete!")
        print(f"{'='*60}")
        print(f"Status: {result.status.value}")
        print(f"Quality Score: {result.quality_score or 'N/A'}")
        print(f"Sources Found: {len(result.sources)}")
        print(f"Iterations: {result.iterations}")
        print(f"Execution Time: {result.execution_time_seconds:.2f}s")
        
        if result.report:
            print(f"\n{'='*60}")
            print(f"Research Report")
            print(f"{'='*60}\n")
            print(result.report[:2000])
            
            if len(result.report) > 2000:
                print("\n... (report truncated)")
        
        if result.errors:
            print(f"\nErrors encountered:")
            for error in result.errors:
                print(f"  - {error}")
        
    except Exception as e:
        logger.error(f"Research failed: {e}")
        print(f"\n❌ Research failed: {e}")
    
    logger.info("Application finished")


def main():
    """Main entry point."""
    try:
        asyncio.run(run_cli())
    except KeyboardInterrupt:
        print("\n\n⚠️ Research cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()