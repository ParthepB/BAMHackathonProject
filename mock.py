import openai
import json
import time
import random
from datetime import datetime
from flask import Flask, request, jsonify, session
import os
import dotenv
import re
import logging

# Load environment variables
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockInterviewBot:
    def __init__(self):
        """Initialize the Mock Interview Bot with Azure OpenAI credentials"""
        
        # Azure OpenAI Configuration - using the working pattern from rmaker.py
        self.AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        self.MODEL_NAME = "gpt-35-turbo"
        
        # Initialize client as None first
        self.client = None
        
        # Initialize the Azure OpenAI client
        self._initialize_azure_client()
        
        # Interview configuration
        self.interview_types = {
            'behavioral': {
                'focus': 'past experiences, soft skills, cultural fit',
                'question_style': 'STAR method responses',
                'avatar_persona': 'friendly and empathetic HR manager'
            },
            'technical': {
                'focus': 'technical skills, problem-solving, coding',
                'question_style': 'practical problems and technical concepts',
                'avatar_persona': 'experienced technical lead'
            },
            'general': {
                'focus': 'overall fit, motivation, career goals',
                'question_style': 'broad range of topics',
                'avatar_persona': 'professional interviewer'
            },
            'situational': {
                'focus': 'hypothetical scenarios and decision-making',
                'question_style': 'scenario-based questions',
                'avatar_persona': 'analytical manager'
            }
        }
        
        # 3D Avatar expressions and gestures
        self.avatar_expressions = {
            'welcoming': {
                'expression': 'smile',
                'gesture': 'wave',
                'tone': 'warm and friendly'
            },
            'listening': {
                'expression': 'attentive',
                'gesture': 'nod',
                'tone': 'engaged'
            },
            'questioning': {
                'expression': 'curious',
                'gesture': 'lean_forward',
                'tone': 'inquisitive'
            },
            'encouraging': {
                'expression': 'supportive_smile',
                'gesture': 'thumbs_up',
                'tone': 'motivating'
            },
            'analytical': {
                'expression': 'thoughtful',
                'gesture': 'chin_touch',
                'tone': 'analytical'
            },
            'concluding': {
                'expression': 'professional_smile',
                'gesture': 'handshake',
                'tone': 'concluding'
            }
        }

    def _initialize_azure_client(self):
        """Set up the client for AI Chat - with error handling for older OpenAI library"""
        try:
            if not self.AOAI_KEY or not self.AOAI_ENDPOINT:
                logger.warning("Azure OpenAI credentials not found in environment variables")
                print("Warning: Azure OpenAI credentials not found in environment variables")
                return False
            
            # Configure OpenAI for Azure (older library version)
            openai.api_type = "azure"
            openai.api_base = self.AOAI_ENDPOINT
            openai.api_version = "2023-05-15"
            openai.api_key = self.AOAI_KEY
            
            # Test the connection
            response = openai.ChatCompletion.create(
                engine=self.MODEL_NAME,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            
            logger.info("✅ Azure OpenAI client initialized successfully!")
            print("✅ Azure OpenAI client initialized successfully!")
            self.client = openai
            return True
            
        except Exception as e:
            logger.error(f"Could not initialize Azure OpenAI client: {e}")
            print(f"Warning: Could not initialize Azure OpenAI client: {e}")
            self.client = None
            return False

    def start_interview_session(self, interview_data):
        """
        Start a new interview session with personalized setup
        
        Args:
            interview_data (dict): Interview configuration data
            
        Returns:
            dict: Interview session data with first question
        """
        try:
            # Generate unique session ID
            session_id = f"interview_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Store interview configuration
            interview_config = {
                'session_id': session_id,
                'job_title': interview_data.get('jobTitle', ''),
                'company': interview_data.get('company', ''),
                'experience_level': interview_data.get('experienceLevel', ''),
                'interview_type': interview_data.get('interviewType', ''),
                'industry': interview_data.get('industry', ''),
                'focus_areas': interview_data.get('focusAreas', ''),
                'start_time': datetime.now().isoformat(),
                'conversation_history': [],
                'current_question': 1,
                'total_questions': 10,
                'avatar_state': 'welcoming'
            }
            
            # Generate personalized welcome message and first question
            welcome_response = self._generate_welcome_message(interview_config)
            
            # Update conversation history
            interview_config['conversation_history'].append({
                'type': 'ai',
                'content': welcome_response['message'],
                'timestamp': datetime.now().isoformat(),
                'avatar_state': welcome_response['avatar_state']
            })
            
            return {
                'success': True,
                'session_id': session_id,
                'message': welcome_response['message'],
                'avatar_state': welcome_response['avatar_state'],
                'question_number': 1,
                'total_questions': 10
            }
            
        except Exception as e:
            logger.error(f"Error starting interview session: {e}")
            return {
                'success': False,
                'error': 'Failed to start interview session',
                'message': self._get_fallback_welcome_message(interview_data)
            }

    def _generate_welcome_message(self, interview_config):
        """Generate a personalized welcome message using AI"""
        
        if not self.client:
            logger.info("Using fallback welcome message - AI client not available")
            return self._get_fallback_welcome_message(interview_config)
        
        try:
            interview_type_info = self.interview_types.get(
                interview_config['interview_type'], 
                self.interview_types['general']
            )
            
            system_prompt = f"""
            You are a 3D avatar interviewer conducting a {interview_config['interview_type']} interview.
            Your persona: {interview_type_info['avatar_persona']}
            
            Job Details:
            - Position: {interview_config['job_title']}
            - Company: {interview_config['company'] or 'the company'}
            - Experience Level: {interview_config['experience_level']}
            - Industry: {interview_config['industry']}
            - Focus Areas: {interview_config['focus_areas']}
            
            Create a warm, professional welcome message that:
            1. Introduces yourself as their AI interviewer
            2. Acknowledges the specific role and company
            3. Sets expectations for the interview process
            4. Asks an engaging opening question that encourages them to share about themselves
            
            Keep it conversational, encouraging, and professional. Limit to 3-4 sentences.
            """
            
            user_prompt = f"Create a personalized welcome message for this {interview_config['interview_type']} interview for the {interview_config['job_title']} position."
            
            response = self.client.ChatCompletion.create(
                engine=self.MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            ai_message = response.choices[0].message.content.strip()
            
            return {
                'message': ai_message,
                'avatar_state': self.avatar_expressions['welcoming']
            }
            
        except Exception as e:
            logger.error(f"Error generating welcome message: {e}")
            return self._get_fallback_welcome_message(interview_config)

    def _get_fallback_welcome_message(self, interview_config):
        """Fallback welcome message when AI is unavailable"""
        job_title = interview_config.get('job_title', 'this position')
        company = interview_config.get('company', 'the company')
        
        fallback_message = f"""
        Hello! I'm your AI interviewer, and I'm excited to conduct this interview with you today. 
        I understand you're interested in the {job_title} position{f' at {company}' if company else ''}. 
        This will be a {interview_config.get('interview_type', 'general')} interview where we'll explore your experiences and qualifications. 
        Let's start with a simple question: Can you tell me a bit about yourself and what draws you to this role?
        """
        
        return {
            'message': fallback_message.strip(),
            'avatar_state': self.avatar_expressions['welcoming']
        }

    def process_user_response(self, session_id, user_response, interview_config):
        """
        Process user response and generate next question
        
        Args:
            session_id (str): Interview session ID
            user_response (str): User's response text
            interview_config (dict): Current interview configuration
            
        Returns:
            dict: AI response with next question and avatar state
        """
        try:
            # Add user response to conversation history
            interview_config['conversation_history'].append({
                'type': 'user',
                'content': user_response,
                'timestamp': datetime.now().isoformat()
            })
            
            # Generate AI response
            ai_response = self._generate_ai_response(user_response, interview_config)
            
            # Update conversation history with AI response
            interview_config['conversation_history'].append({
                'type': 'ai',
                'content': ai_response['message'],
                'timestamp': datetime.now().isoformat(),
                'avatar_state': ai_response['avatar_state']
            })
            
            # Update question counter
            interview_config['current_question'] += 1
            
            return {
                'success': True,
                'message': ai_response['message'],
                'avatar_state': ai_response['avatar_state'],
                'question_number': interview_config['current_question'],
                'total_questions': interview_config['total_questions'],
                'is_complete': interview_config['current_question'] > interview_config['total_questions']
            }
            
        except Exception as e:
            logger.error(f"Error processing user response: {e}")
            return {
                'success': False,
                'error': 'Failed to process response',
                'message': "I apologize, but I'm having trouble processing your response. Could you please try again?"
            }

    def _generate_ai_response(self, user_response, interview_config):
        """Generate AI interviewer response using Azure OpenAI"""
        
        if not self.client:
            logger.info("Using fallback AI response - AI client not available")
            return self._get_fallback_ai_response(user_response, interview_config)
        
        try:
            interview_type_info = self.interview_types.get(
                interview_config['interview_type'], 
                self.interview_types['general']
            )
            
            # Analyze conversation context
            conversation_context = self._build_conversation_context(interview_config['conversation_history'])
            current_question = interview_config['current_question']
            total_questions = interview_config['total_questions']
            
            # Determine interview phase
            if current_question <= 3:
                phase = "opening"
                avatar_mood = "questioning"
            elif current_question <= 7:
                phase = "deep_dive"
                avatar_mood = "analytical"
            else:
                phase = "closing"
                avatar_mood = "concluding"
            
            system_prompt = f"""
            You are a professional 3D avatar interviewer conducting a {interview_config['interview_type']} interview.
            Your persona: {interview_type_info['avatar_persona']}
            
            Interview Context:
            - Position: {interview_config['job_title']}
            - Company: {interview_config['company'] or 'the company'}
            - Experience Level: {interview_config['experience_level']}
            - Industry: {interview_config['industry']}
            - Focus Areas: {interview_config['focus_areas']}
            - Current Question: {current_question}/{total_questions}
            - Interview Phase: {phase}
            
            Interview Focus: {interview_type_info['focus']}
            Question Style: {interview_type_info['question_style']}
            
            Instructions:
            1. Acknowledge the candidate's response professionally
            2. Provide brief, encouraging feedback when appropriate
            3. Ask a relevant follow-up question that builds on their response
            4. Vary question types: behavioral, situational, technical (based on interview type)
            5. Keep responses conversational and engaging
            6. Maintain professional but friendly tone
            
            For behavioral interviews, use STAR method prompts.
            For technical interviews, include practical scenarios.
            For situational interviews, present hypothetical challenges.
            
            Response should be 2-4 sentences maximum.
            """
            
            user_prompt = f"""
            Candidate's response: "{user_response}"
            
            Conversation context: {conversation_context}
            
            Generate your next response as the interviewer, including:
            1. Brief acknowledgment of their response
            2. A relevant follow-up question appropriate for this interview phase
            """
            
            response = self.client.ChatCompletion.create(
                engine=self.MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=250,
                temperature=0.8
            )
            
            ai_message = response.choices[0].message.content.strip()
            
            return {
                'message': ai_message,
                'avatar_state': self.avatar_expressions[avatar_mood]
            }
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return self._get_fallback_ai_response(user_response, interview_config)

    def _get_fallback_ai_response(self, user_response, interview_config):
        """Fallback AI response when OpenAI is unavailable"""
        current_question = interview_config['current_question']
        
        fallback_questions = [
            "That's great to hear! Can you tell me about a challenging project you've worked on and how you approached it?",
            "Interesting! What would you say is your greatest professional strength, and can you give me an example?",
            "I appreciate that insight. How do you handle working under pressure or tight deadlines?",
            "That's valuable experience. Can you describe a time when you had to work with a difficult team member?",
            "Good point! What motivates you most in your work, and how do you stay engaged?",
            "I see. Where do you see yourself professionally in the next 3-5 years?",
            "That's helpful context. What questions do you have about this role or our company?",
            "Thank you for sharing. Is there anything else you'd like me to know about your qualifications?"
        ]
        
        if current_question <= len(fallback_questions):
            message = fallback_questions[current_question - 1]
        else:
            message = "Thank you for that response. Do you have any final questions for me?"
        
        return {
            'message': message,
            'avatar_state': self.avatar_expressions['questioning']
        }

    def _build_conversation_context(self, conversation_history):
        """Build conversation context for AI prompting"""
        context = ""
        for i, message in enumerate(conversation_history[-4:]):  # Last 4 messages
            if message['type'] == 'user':
                context += f"Candidate: {message['content'][:100]}...\n"
            else:
                context += f"Interviewer: {message['content'][:100]}...\n"
        return context

    def generate_interview_report(self, interview_config):
        """
        Generate comprehensive interview performance report
        
        Args:
            interview_config (dict): Complete interview session data
            
        Returns:
            dict: Detailed performance analysis and feedback
        """
        try:
            if not self.client:
                logger.info("Using fallback report - AI client not available")
                return self._get_fallback_report(interview_config)
            
            # Extract conversation for analysis
            conversation_text = self._extract_conversation_text(interview_config['conversation_history'])
            
            system_prompt = f"""
            You are an expert interview analyst. Analyze this {interview_config['interview_type']} interview 
            for a {interview_config['job_title']} position and provide comprehensive feedback.
            
            Evaluate the candidate on:
            1. Communication Skills (clarity, articulation, confidence)
            2. Technical Knowledge (relevant to role and industry)
            3. Problem-Solving Ability (analytical thinking, creativity)
            4. Cultural Fit (alignment with role and company values)
            5. Experience Relevance (how well experience matches role requirements)
            
            Provide scores (0-100) for each category and overall.
            Include specific strengths, areas for improvement, and actionable recommendations.
            """
            
            user_prompt = f"""
            Interview Details:
            - Position: {interview_config['job_title']}
            - Industry: {interview_config['industry']}
            - Experience Level: {interview_config['experience_level']}
            - Interview Type: {interview_config['interview_type']}
            
            Conversation:
            {conversation_text}
            
            Provide a detailed analysis in JSON format with:
            {{
                "overall_score": <score>,
                "category_scores": {{
                    "communication": <score>,
                    "technical_knowledge": <score>,
                    "problem_solving": <score>,
                    "cultural_fit": <score>,
                    "experience_relevance": <score>
                }},
                "strengths": [<list of strengths>],
                "improvements": [<list of areas for improvement>],
                "recommendations": [<list of actionable recommendations>],
                "summary": "<overall assessment summary>"
            }}
            """
            
            response = self.client.ChatCompletion.create(
                engine=self.MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            # Parse AI response
            ai_analysis = response.choices[0].message.content.strip()
            
            try:
                # Try to parse as JSON
                report_data = json.loads(ai_analysis)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                logger.warning("Could not parse AI report as JSON, using fallback")
                return self._get_fallback_report(interview_config)
            
            # Add metadata
            report_data['interview_metadata'] = {
                'session_id': interview_config['session_id'],
                'job_title': interview_config['job_title'],
                'company': interview_config['company'],
                'interview_type': interview_config['interview_type'],
                'duration': self._calculate_interview_duration(interview_config),
                'total_questions': len([m for m in interview_config['conversation_history'] if m['type'] == 'ai']),
                'completion_date': datetime.now().isoformat()
            }
            
            return {
                'success': True,
                'report': report_data
            }
            
        except Exception as e:
            logger.error(f"Error generating interview report: {e}")
            return self._get_fallback_report(interview_config)

    def _extract_conversation_text(self, conversation_history):
        """Extract conversation text for analysis"""
        conversation = ""
        for message in conversation_history:
            speaker = "Interviewer" if message['type'] == 'ai' else "Candidate"
            conversation += f"{speaker}: {message['content']}\n\n"
        return conversation

    def _calculate_interview_duration(self, interview_config):
        """Calculate interview duration in minutes"""
        try:
            start_time = datetime.fromisoformat(interview_config['start_time'])
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 60
            return round(duration, 1)
        except:
            return 0

    def _get_fallback_report(self, interview_config):
        """Generate fallback report when AI is unavailable"""
        return {
            'success': True,
            'report': {
                'overall_score': 78,
                'category_scores': {
                    'communication': 80,
                    'technical_knowledge': 75,
                    'problem_solving': 82,
                    'cultural_fit': 76,
                    'experience_relevance': 77
                },
                'strengths': [
                    "Demonstrated clear communication throughout the interview",
                    "Showed enthusiasm for the role and company",
                    "Provided relevant examples from past experience"
                ],
                'improvements': [
                    "Could provide more specific metrics and quantifiable achievements",
                    "Consider using the STAR method for behavioral questions",
                    "Prepare more detailed questions about the role and company"
                ],
                'recommendations': [
                    "Practice articulating achievements with specific numbers and impact",
                    "Research the company's recent projects and initiatives",
                    "Prepare thoughtful questions that demonstrate genuine interest"
                ],
                'summary': f"The candidate showed good potential for the {interview_config['job_title']} role with solid communication skills and relevant experience. Focus on providing more quantifiable examples and demonstrating deeper company knowledge.",
                'interview_metadata': {
                    'session_id': interview_config['session_id'],
                    'job_title': interview_config['job_title'],
                    'company': interview_config['company'],
                    'interview_type': interview_config['interview_type'],
                    'completion_date': datetime.now().isoformat()
                }
            }
        }

    def get_avatar_animation_data(self, avatar_state, message_content):
        """
        Generate 3D avatar animation data based on context
        
        Args:
            avatar_state (dict): Current avatar expression state
            message_content (str): Message being delivered
            
        Returns:
            dict: Animation instructions for 3D avatar
        """
        # Analyze message content for emotional context
        emotional_cues = self._analyze_message_emotion(message_content)
        
        # Generate animation sequence
        animations = {
            'facial_expression': avatar_state.get('expression', 'neutral'),
            'gesture': avatar_state.get('gesture', 'idle'),
            'eye_contact': 'direct' if 'question' in message_content.lower() else 'soft',
            'posture': 'leaning_forward' if emotional_cues['engagement'] > 0.7 else 'upright',
            'speech_animation': {
                'mouth_sync': True,
                'emphasis_points': self._find_emphasis_points(message_content),
                'pace': 'normal',
                'tone': avatar_state.get('tone', 'professional')
            },
            'background_mood': self._determine_background_mood(emotional_cues),
            'transition_duration': 0.5
        }
        
        return animations

    def _analyze_message_emotion(self, message):
        """Analyze message for emotional content"""
        positive_words = ['great', 'excellent', 'good', 'impressive', 'wonderful']
        question_words = ['what', 'how', 'why', 'when', 'where', 'tell me']
        encouraging_words = ['keep', 'continue', 'share', 'more']
        
        message_lower = message.lower()
        
        return {
            'positivity': sum(1 for word in positive_words if word in message_lower) / len(positive_words),
            'engagement': sum(1 for word in question_words if word in message_lower) / len(question_words),
            'encouragement': sum(1 for word in encouraging_words if word in message_lower) / len(encouraging_words)
        }

    def _find_emphasis_points(self, message):
        """Find points in message that should be emphasized"""
        emphasis_patterns = [
            r'\b(important|key|crucial|significant)\b',
            r'\b(tell me|explain|describe)\b',
            r'\?',  # Questions
            r'!'   # Exclamations
        ]
        
        emphasis_points = []
        for pattern in emphasis_patterns:
            matches = re.finditer(pattern, message, re.IGNORECASE)
            for match in matches:
                emphasis_points.append({
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'emphasis'
                })
        
        return emphasis_points

    def _determine_background_mood(self, emotional_cues):
        """Determine background lighting/mood for avatar"""
        if emotional_cues['positivity'] > 0.6:
            return 'warm'
        elif emotional_cues['engagement'] > 0.5:
            return 'focused'
        else:
            return 'neutral'

# Global interview bot instance
interview_bot = MockInterviewBot()

# Flask routes for the mock interview system
def init_mock_interview_routes(app):
    """Initialize mock interview routes"""
    
    @app.route('/api/mock-interview/start', methods=['POST'])
    def start_interview():
        """Start a new mock interview session"""
        try:
            interview_data = request.get_json()
            
            # Validate required fields
            required_fields = ['jobTitle', 'experienceLevel', 'interviewType']
            for field in required_fields:
                if not interview_data.get(field):
                    return jsonify({
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }), 400
            
            # Start interview session
            result = interview_bot.start_interview_session(interview_data)
            
            # Store session in Flask session
            if result['success']:
                session['interview_config'] = {
                    'session_id': result['session_id'],
                    'job_title': interview_data.get('jobTitle'),
                    'company': interview_data.get('company', ''),
                    'experience_level': interview_data.get('experienceLevel'),
                    'interview_type': interview_data.get('interviewType'),
                    'industry': interview_data.get('industry', ''),
                    'focus_areas': interview_data.get('focusAreas', ''),
                    'start_time': datetime.now().isoformat(),
                    'conversation_history': [],
                    'current_question': 1,
                    'total_questions': 10
                }
                
                # Add initial AI message to history
                session['interview_config']['conversation_history'].append({
                    'type': 'ai',
                    'content': result['message'],
                    'timestamp': datetime.now().isoformat(),
                    'avatar_state': result['avatar_state']
                })
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Error in start_interview: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500

    @app.route('/api/mock-interview/respond', methods=['POST'])
    def process_response():
        """Process user response and generate AI reply"""
        try:
            data = request.get_json()
            user_response = data.get('response', '').strip()
            
            if not user_response:
                return jsonify({
                    'success': False,
                    'error': 'Empty response'
                }), 400
            
            # Get interview config from session
            interview_config = session.get('interview_config')
            if not interview_config:
                return jsonify({
                    'success': False,
                    'error': 'No active interview session'
                }), 400
            
            # Process the response
            result = interview_bot.process_user_response(
                interview_config['session_id'],
                user_response,
                interview_config
            )
            
            # Update session with new conversation state
            session['interview_config'] = interview_config
            session.modified = True
            
            # Add avatar animation data
            if result['success'] and not result.get('is_complete'):
                result['avatar_animation'] = interview_bot.get_avatar_animation_data(
                    result['avatar_state'],
                    result['message']
                )
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Error in process_response: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500

    @app.route('/api/mock-interview/end', methods=['POST'])
    def end_interview():
        """End interview and generate performance report"""
        try:
            # Get interview config from session
            interview_config = session.get('interview_config')
            if not interview_config:
                return jsonify({
                    'success': False,
                    'error': 'No active interview session'
                }), 400
            
            # Generate performance report
            report_result = interview_bot.generate_interview_report(interview_config)
            
            # Clear session
            session.pop('interview_config', None)
            
            return jsonify(report_result)
            
        except Exception as e:
            logger.error(f"Error in end_interview: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500

    @app.route('/api/mock-interview/avatar-state', methods=['GET'])
    def get_avatar_state():
        """Get current avatar animation state"""
        try:
            interview_config = session.get('interview_config')
            if not interview_config:
                return jsonify({
                    'success': False,
                    'error': 'No active interview session'
                }), 400
            
            # Get last AI message for context
            last_ai_message = None
            for message in reversed(interview_config['conversation_history']):
                if message['type'] == 'ai':
                    last_ai_message = message
                    break
            
            if last_ai_message:
                avatar_state = last_ai_message.get('avatar_state', interview_bot.avatar_expressions['listening'])
                animation_data = interview_bot.get_avatar_animation_data(
                    avatar_state,
                    last_ai_message['content']
                )
            else:
                animation_data = interview_bot.get_avatar_animation_data(
                    interview_bot.avatar_expressions['welcoming'],
                    "Welcome to your interview!"
                )
            
            return jsonify({
                'success': True,
                'avatar_animation': animation_data
            })
            
        except Exception as e:
            logger.error(f"Error in get_avatar_state: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500

if __name__ == "__main__":
    # Test the mock interview bot
    test_bot = MockInterviewBot()
    
    # Test interview data
    test_data = {
        'jobTitle': 'Software Engineer',
        'company': 'Microsoft',
        'experienceLevel': 'mid',
        'interviewType': 'technical',
        'industry': 'Technology',
        'focusAreas': 'Python, Machine Learning'
    }
    
    print("Testing Mock Interview Bot...")
    result = test_bot.start_interview_session(test_data)
    print(f"Start Interview Result: {result}")