import openai
from typing import AsyncGenerator, Optional
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()


class OpenAIService:
    """Service class for interacting with OpenAI API."""
    
    def __init__(self):
        """Initialize the OpenAI service with API key."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.async_client = openai.AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input prompt for generation
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise
    
    async def agenerate(self, prompt: str, **kwargs) -> str:
        """Async generate text from a prompt."""
        try:
            response = await self.async_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise
    
    async def agenerate_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """
        Stream text generation.
        
        Args:
            prompt: Input prompt for generation
            **kwargs: Additional generation parameters
            
        Yields:
            Text chunks as they're generated
        """
        try:
            response = await self.async_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                **kwargs
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"OpenAI streaming failed: {e}")
            raise
    
    async def generate_with_timeout(
        self,
        prompt: str,
        timeout_seconds: float = 30.0,
        **kwargs
    ) -> str:
        """
        Generate text with timeout.
        
        Args:
            prompt: Input prompt for generation
            timeout_seconds: Maximum time to wait for response
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
            
        Raises:
            TimeoutError: If generation exceeds timeout
        """
        import asyncio
        
        try:
            return await asyncio.wait_for(
                self.agenerate(prompt, **kwargs),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            raise TimeoutError(f"OpenAI generation timed out after {timeout_seconds}s")


# Singleton instance
openai_service = OpenAIService()
