from flask import Flask, send_from_directory, request, jsonify
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
MODEL_NAME = "gpt-35-turbo"

# Initialize client as None first
client = None

# Set up the client for AI Chat - with error handling
def initialize_azure_client():
    global client
    try:
        if not AOAI_KEY or not AOAI_ENDPOINT:
            print("Warning: Azure OpenAI credentials not found in environment variables")
            return False
        
        from openai import AzureOpenAI
        # Simple initialization without test call
        client = AzureOpenAI(
            api_key=AOAI_KEY,
            azure_endpoint=AOAI_ENDPOINT,
            api_version="2023-05-15"
        )
        
        print("Azure OpenAI client initialized successfully")
        return True
    except Exception as e:
        print(f"Warning: Could not initialize Azure OpenAI client: {e}")
        client = None
        return False

# Try to initialize the client
initialize_azure_client()

def generate_resume_section(section_type, user_data):
    """
    Generate a specific section of a resume using Azure OpenAI
    
    Args:
        section_type (str): Type of section (summary, experience, education, skills)
        user_data (dict): User information relevant to that section
    
    Returns:
        str: Generated resume section content
    """
    if client is None:
        # Fallback templates when AI is not available
        fallback_templates = {
            "summary": f"Experienced {user_data.get('target_role', 'professional')} with {user_data.get('experience_years', 'several years')} of experience in {user_data.get('industry', 'the industry')}. Skilled in {user_data.get('technical_skills', 'various technologies')} with a proven track record of delivering results.",
            
            "experience": f"{user_data.get('job_title', 'Professional')}\n{user_data.get('company', 'Company Name')} | {user_data.get('duration', '2020-2023')}\n\n• {user_data.get('responsibilities', 'Managed various responsibilities and duties')}\n• {user_data.get('achievements', 'Achieved notable accomplishments and results')}",
            
            "education": f"{user_data.get('degree', 'Bachelor of Science')}\n{user_data.get('school', 'University Name')}, {user_data.get('grad_year', '2023')}",
            
            "skills": f"Technical Skills: {user_data.get('technical_skills', 'Programming, Software Development')}\nSoft Skills: {user_data.get('soft_skills', 'Communication, Leadership, Problem-solving')}"
        }
        
        return fallback_templates.get(section_type, fallback_templates["summary"])
    
    if not AOAI_KEY or not AOAI_ENDPOINT:
        return f"Azure OpenAI credentials not configured. Please check your .env file."
    
    try:
        prompts = {
            "summary": f"""
            Create a professional resume summary/objective for someone with the following background:
            - Name: {user_data.get('name', 'Professional')}
            - Job Title/Target Role: {user_data.get('target_role', 'Professional')}
            - Years of Experience: {user_data.get('experience_years', 'Entry level')}
            - Key Skills: {user_data.get('key_skills', 'Various skills')}
            - Industry: {user_data.get('industry', 'General')}
            
            Write a compelling 2-3 sentence professional summary that highlights their strengths and career goals.
            """,
            
            "experience": f"""
            Create professional work experience entries based on this information:
            - Job Title: {user_data.get('job_title', 'Professional')}
            - Company: {user_data.get('company', 'Company Name')}
            - Duration: {user_data.get('duration', '2020-2023')}
            - Responsibilities: {user_data.get('responsibilities', 'Various responsibilities')}
            - Achievements: {user_data.get('achievements', 'Notable accomplishments')}
            
            Format as a professional work experience entry with bullet points highlighting key responsibilities and achievements. Use action verbs and quantify results where possible.
            """,
            
            "education": f"""
            Create an education section based on:
            - Degree: {user_data.get('degree', 'Degree')}
            - School: {user_data.get('school', 'University')}
            - Graduation Year: {user_data.get('grad_year', '2023')}
            - GPA: {user_data.get('gpa', '')}
            - Relevant Coursework: {user_data.get('coursework', '')}
            
            Format as a clean education entry suitable for a resume.
            """,
            
            "skills": f"""
            Organize and format these skills into professional categories:
            - Technical Skills: {user_data.get('technical_skills', '')}
            - Soft Skills: {user_data.get('soft_skills', '')}
            - Industry Skills: {user_data.get('industry_skills', '')}
            - Languages: {user_data.get('languages', '')}
            
            Format as a well-organized skills section with appropriate categories and bullet points.
            """
        }
        
        prompt = prompts.get(section_type, prompts["summary"])
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional resume writer with expertise in creating compelling, ATS-friendly resume content. Focus on clarity, impact, and professional formatting."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error generating {section_type} section: {str(e)}")
        # Fallback to template if AI fails
        fallback_templates = {
            "summary": f"Experienced {user_data.get('target_role', 'professional')} with {user_data.get('experience_years', 'several years')} of experience in {user_data.get('industry', 'the industry')}. Skilled in {user_data.get('technical_skills', 'various technologies')} with a proven track record of delivering results.",
            
            "experience": f"{user_data.get('job_title', 'Professional')}\n{user_data.get('company', 'Company Name')} | {user_data.get('duration', '2020-2023')}\n\n• {user_data.get('responsibilities', 'Managed various responsibilities and duties')}\n• {user_data.get('achievements', 'Achieved notable accomplishments and results')}",
            
            "education": f"{user_data.get('degree', 'Bachelor of Science')}\n{user_data.get('school', 'University Name')}, {user_data.get('grad_year', '2023')}",
            
            "skills": f"Technical Skills: {user_data.get('technical_skills', 'Programming, Software Development')}\nSoft Skills: {user_data.get('soft_skills', 'Communication, Leadership, Problem-solving')}"
        }
        
        return fallback_templates.get(section_type, fallback_templates["summary"])

def generate_full_resume(user_data):
    """
    Generate a complete resume using Azure OpenAI
    
    Args:
        user_data (dict): Complete user information
    
    Returns:
        dict: Complete resume with all sections
    """
    try:
        # Generate each section
        summary = generate_resume_section("summary", user_data)
        
        # Handle multiple work experiences
        experiences = []
        if isinstance(user_data.get('work_experience'), list):
            for exp in user_data['work_experience']:
                experience = generate_resume_section("experience", exp)
                experiences.append(experience)
        else:
            experience = generate_resume_section("experience", user_data)
            experiences.append(experience)
        
        education = generate_resume_section("education", user_data)
        skills = generate_resume_section("skills", user_data)
        
        return {
            "success": True,
            "resume": {
                "personal_info": {
                    "name": user_data.get('name', ''),
                    "email": user_data.get('email', ''),
                    "phone": user_data.get('phone', ''),
                    "address": user_data.get('address', ''),
                    "linkedin": user_data.get('linkedin', ''),
                    "portfolio": user_data.get('portfolio', '')
                },
                "summary": summary,
                "experience": experiences,
                "education": education,
                "skills": skills
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to generate resume: {str(e)}"
        }

def improve_resume_content(existing_content, improvement_focus="general"):
    """
    Improve existing resume content using AI
    
    Args:
        existing_content (str): Current resume content
        improvement_focus (str): Area to focus on (keywords, impact, clarity, etc.)
    
    Returns:
        str: Improved resume content
    """
    try:
        focus_prompts = {
            "keywords": "Focus on adding relevant industry keywords and ATS-friendly terms.",
            "impact": "Focus on quantifying achievements and demonstrating measurable impact.",
            "clarity": "Focus on improving clarity, readability, and professional language.",
            "general": "Provide overall improvements to make the content more professional and impactful."
        }
        
        focus_instruction = focus_prompts.get(improvement_focus, focus_prompts["general"])
        
        prompt = f"""
        Please improve the following resume content:
        
        {existing_content}
        
        Improvement focus: {focus_instruction}
        
        Provide the improved version with better formatting, stronger action verbs, and more professional language.
        """
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert resume writer. Improve the given content while maintaining accuracy and professional standards."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.6
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Unable to improve content: {str(e)}"
