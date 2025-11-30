"""
Chat Service Implementation with Fine-tuned Qwen Model
CPU-OPTIMIZED VERSION - No quantization needed for CPU
"""
import sys
import os
from typing import Dict, List
import logging
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
# Setup logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import AI libraries
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    logger.info("✅ PyTorch and Transformers imported")
except ImportError as e:
    logger.error(f"❌ Failed to import AI libraries: {e}")
    logger.error("Install with: pip install torch transformers")
    raise

# Import config with better error handling
try:
    from backend.config import settings
except ImportError:
    try:
        from ..config import settings
    except ImportError:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        sys.path.insert(0, project_root)
        from backend.config import settings

logger.info(f"✅ Config loaded: {settings.MODEL_NAME}")


class ChatMessage:
    """Simple message class"""
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
    
    def __repr__(self):
        return f"ChatMessage(role={self.role}, content={self.content[:50]}...)"


class SimpleChatHistory:
    """Simple in-memory chat history"""
    def __init__(self):
        self.messages: List[ChatMessage] = []
    
    def add_user_message(self, message: str):
        """Add user message"""
        self.messages.append(ChatMessage("user", message))
        logger.debug(f"Added user message: {message[:50]}...")
    
    def add_ai_message(self, message: str):
        """Add AI message"""
        self.messages.append(ChatMessage("assistant", message))
        logger.debug(f"Added AI message: {message[:50]}...")
    
    def clear(self):
        """Clear all messages"""
        count = len(self.messages)
        self.messages = []
        logger.debug(f"Cleared {count} messages")
    
    def __len__(self):
        return len(self.messages)


class ChatService:
    """
    Chat Service with Fine-tuned Qwen Model
    CPU-OPTIMIZED - No quantization for simpler setup
    """
    
    def __init__(self):
        """Initialize chat service"""
        logger.info("="*70)
        logger.info("🚀 INITIALIZING CHAT SERVICE")
        logger.info("="*70)
        
        self.session_store: Dict[str, SimpleChatHistory] = {}
        self.session_created: Dict[str, str] = {}
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        
        # Determine device
        self.device = self._get_device()
        
        # Load model
        self._load_model()
        
        logger.info("="*70)
        if self.model_loaded:
            logger.info("✅ CHAT SERVICE INITIALIZED SUCCESSFULLY")
        else:
            logger.error("❌ CHAT SERVICE INITIALIZATION FAILED")
        logger.info("="*70)
    
    def _get_device(self) -> str:
        """Determine the best available device"""
        try:
            if settings.MODEL_DEVICE.lower() == "cuda" and torch.cuda.is_available():
                device = "cuda"
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                logger.info(f"🎮 Using GPU: {gpu_name}")
                logger.info(f"💾 GPU Memory: {gpu_memory:.1f} GB")
            else:
                device = "cpu"
                logger.info("💻 Using CPU")
                if settings.MODEL_DEVICE.lower() == "cuda":
                    logger.warning("⚠️  CUDA requested but not available, using CPU")
            return device
        except Exception as e:
            logger.warning(f"⚠️ Error detecting device, defaulting to CPU: {e}")
            return "cpu"
    
    def _load_model(self):
        """
        Load Fine-tuned Qwen Model from LOCAL directory
        FINAL WORKING VERSION - Handles 8-bit quantization
        """
        try:
            model_name = settings.MODEL_NAME
            logger.info(f"📥 Loading model: {model_name}")
            logger.info("⏳ This may take 1-2 minutes...")
            
            # Check if model path exists
            if not os.path.exists(model_name):
                raise FileNotFoundError(
                    f"Model not found at: {model_name}\n"
                    f"Make sure the model folder exists with config.json and model files"
                )
            
            logger.info(f"✅ Found local model at: {model_name}")
            
            # STEP 1: Load tokenizer
            logger.info("🔤 Step 1/2: Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True,
                local_files_only=True
            )
            
            # Set padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                logger.debug("Set pad_token = eos_token")
            
            logger.info("✅ Tokenizer loaded successfully")
            
            # STEP 2: Load model (8-bit quantized)
            logger.info("🤖 Step 2/2: Loading model...")
            logger.info(f"   Target device: {self.device}")
            logger.info("   Model is 8-bit quantized (will load automatically)")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                low_cpu_mem_usage=True,
                local_files_only=True
                # device_map and dtype handled automatically for quantized models
            )
            
            # DON'T call .to() for quantized models - they handle device themselves
            logger.info(f"✅ Model loaded successfully (8-bit quantized)")
            
            # Set to evaluation mode
            self.model.eval()
            
            # Calculate model stats
            param_count = sum(p.numel() for p in self.model.parameters())
            
            logger.info("✅ Model ready for inference!")
            logger.info(f"📊 Model stats:")
            logger.info(f"   Parameters: {param_count:,} ({param_count/1e9:.2f}B)")
            try:
                logger.info(f"   Device: {next(self.model.parameters()).device}")
                logger.info(f"   Dtype: {next(self.model.parameters()).dtype}")
            except:
                logger.info(f"   Device: Multiple (8-bit uses special placement)")
            
            self.model_loaded = True
            
        except Exception as e:
            logger.error("="*70)
            logger.error("❌ MODEL LOADING FAILED")
            logger.error(f"Error: {str(e)}")
            
            import traceback
            logger.error("Full error traceback:")
            logger.error(traceback.format_exc())
            
            logger.error("="*70)
            logger.error("💡 Troubleshooting tips:")
            logger.error(f"   1. Check model path exists: {settings.MODEL_NAME}")
            logger.error("   2. Ensure bitsandbytes is installed: pip install bitsandbytes")
            logger.error("   3. Ensure model files (*.safetensors or *.bin) are present")
            logger.error("   4. Check you have ~4GB free RAM (8-bit saves memory)")
            logger.error("="*70)
            self.model_loaded = False
            raise


    def is_model_loaded(self) -> bool:
        """Check if model is ready"""
        return self.model_loaded and self.model is not None
    
    def get_session_history(self, session_id: str) -> SimpleChatHistory:
        """Get or create session history"""
        if session_id not in self.session_store:
            self.session_store[session_id] = SimpleChatHistory()
            self.session_created[session_id] = datetime.now().isoformat()
            logger.info(f"📝 Created new session: {session_id}")
        return self.session_store[session_id]
    
    def _format_conversation(self, history: SimpleChatHistory, prompt: str) -> List[Dict[str, str]]:
        """Format conversation for Qwen"""
        messages = []
        
        # Add system message for world history
        messages.append({
            "role": "system",
            "content": "You are a knowledgeable world history expert. Provide accurate, detailed, and engaging historical information."
        })
        
        # Add history
        for msg in history.messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Limit history
        max_messages = settings.MAX_HISTORY_LENGTH * 2 + 1  # +1 for system message
        if len(messages) > max_messages:
            # Keep system message and most recent history
            system_msg = messages[0]
            recent_msgs = messages[-(max_messages-1):]
            messages = [system_msg] + recent_msgs
            logger.debug(f"Trimmed to {len(messages)} messages")
        
        logger.debug(f"Formatted {len(messages)} messages for model")
        return messages
    
    def _generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate AI response"""
        try:
            logger.debug("🤔 Generating response...")
            
            # Apply chat template
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            logger.debug(f"Prompt length: {len(text)} chars")
            
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=2048
            ).to(self.device)
            
            input_length = inputs['input_ids'].shape[1]
            logger.debug(f"Input tokens: {input_length}")
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=settings.MAX_TOKENS,
                    temperature=settings.TEMPERATURE,
                    top_p=settings.TOP_P,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )
            
            # Extract only the generated tokens
            generated_ids = outputs[0][input_length:]
            response = self.tokenizer.decode(
                generated_ids, 
                skip_special_tokens=True
            ).strip()
            
            logger.debug(f"Generated response: {len(response)} chars")
            
            # Validation
            if not response or len(response) < 5:
                logger.warning("Generated response too short, using fallback")
                return "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
            
            logger.debug(f"Final response length: {len(response)} chars")
            return response
            
        except Exception as e:
            logger.error(f"❌ Generation error: {str(e)}")
            raise RuntimeError(f"Failed to generate response: {str(e)}")
    
    async def chat(self, prompt: str, session_id: str) -> str:
        """Main chat method"""
        if not self.is_model_loaded():
            raise RuntimeError(
                "Model is not loaded. Please check server logs. "
                "The model should load automatically on startup."
            )
        
        logger.info(f"💬 Chat request - Session: {session_id}")
        logger.info(f"📝 Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        
        try:
            # Get history
            history = self.get_session_history(session_id)
            
            # Format messages
            messages = self._format_conversation(history, prompt)
            
            # Generate response
            response = self._generate_response(messages)
            
            # Update history
            history.add_user_message(prompt)
            history.add_ai_message(response)
            
            logger.info(f"✅ Response generated: {len(response)} chars")
            logger.info(f"📊 Session now has {len(history)} messages")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Chat error: {str(e)}")
            raise
    
    def clear_history(self, session_id: str) -> None:
        """Clear session history"""
        if session_id in self.session_store:
            self.session_store[session_id].clear()
            logger.info(f"🗑️ Cleared history: {session_id}")
    
    def delete_session(self, session_id: str) -> None:
        """Delete session"""
        if session_id in self.session_store:
            del self.session_store[session_id]
            if session_id in self.session_created:
                del self.session_created[session_id]
            logger.info(f"🗑️ Deleted session: {session_id}")
    
    def get_message_count(self, session_id: str) -> int:
        """Get message count"""
        if session_id not in self.session_store:
            return 0
        return len(self.session_store[session_id])
    
    def session_exists(self, session_id: str) -> bool:
        """Check if session exists"""
        return session_id in self.session_store
    
    def get_active_sessions_count(self) -> int:
        """Get active session count"""
        return len(self.session_store)
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all sessions"""
        sessions = []
        for session_id in self.session_store.keys():
            sessions.append({
                "session_id": session_id,
                "message_count": self.get_message_count(session_id)
            })
        return sessions
    
    def get_session_created_time(self, session_id: str) -> str:
        """Get session creation time"""
        return self.session_created.get(session_id, datetime.now().isoformat())


# ============================================================================
# GLOBAL INSTANCE INITIALIZATION
# ============================================================================

logger.info("🔨 Initializing global chat_service instance...")

try:
    chat_service = ChatService()
    if chat_service.is_model_loaded():
        logger.info("🎉 Global chat_service ready!")
    else:
        logger.error("⚠️ chat_service created but model not loaded!")
        chat_service = None
except Exception as e:
    logger.error("="*70)
    logger.error("❌ CRITICAL: Failed to initialize chat_service")
    logger.error(f"Error: {str(e)}")
    logger.error("="*70)
    logger.error("The server will start but chat endpoints will not work!")
    logger.error("Please check the errors above and fix the issue.")
    logger.error("="*70)
    chat_service = None

# Export
__all__ = ['chat_service', 'ChatService']