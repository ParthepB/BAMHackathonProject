from flask import Flask, send_from_directory, request, jsonify, render_template
import os
import dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from mock import init_mock_interview_routes

# Load environment variables
dotenv.load_dotenv()
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
MODEL_NAME = "gpt-35-turbo"

# Initialize client as None first
client = None

# Set up the client for AI Chat - with error handling for older OpenAI library
def initialize_azure_client():
    global client
    try:
        if not AOAI_KEY or not AOAI_ENDPOINT:
            print("Warning: Azure OpenAI credentials not found in environment variables")
            return False
        
        import openai
        
        # Configure OpenAI for Azure (older library version)
        openai.api_type = "azure"
        openai.api_base = AOAI_ENDPOINT
        openai.api_version = "2023-05-15"
        openai.api_key = AOAI_KEY
        
        # Test the connection
        response = openai.ChatCompletion.create(
            engine=MODEL_NAME,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        
        print("✅ Azure OpenAI client initialized successfully!")
        client = openai
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
    
    # Debug print for experience section
    if section_type == "experience":
        print(f"DEBUG: Processing {section_type} with data:", user_data.get('experiences', 'No experiences array'))
    
    if client is None:
        # Handle multiple experiences in fallback
        if section_type == "experience":
            # Check for experiences array first
            if user_data.get('experiences'):
                experience_text = ""
                for i, exp in enumerate(user_data['experiences'], 1):
                    if exp.get('job_title') or exp.get('company'):
                        experience_text += f"{exp.get('job_title', 'Professional')}\n"
                        experience_text += f"{exp.get('company', 'Company Name')} | {exp.get('duration', '2020-2023')}\n\n"
                        experience_text += f"• {exp.get('responsibilities', 'Managed various responsibilities and duties')}\n"
                        experience_text += f"• {exp.get('achievements', 'Achieved notable accomplishments and results')}\n"
                        if i < len(user_data['experiences']):
                            experience_text += "\n"
                return experience_text
            else:
                # Fallback to single experience
                return f"{user_data.get('job_title', 'Professional')}\n{user_data.get('company', 'Company Name')} | {user_data.get('duration', '2020-2023')}\n\n• {user_data.get('responsibilities', 'Managed various responsibilities and duties')}\n• {user_data.get('achievements', 'Achieved notable accomplishments and results')}"
        
        # Other fallback templates remain the same...
        fallback_templates = {
            "summary": f"Experienced {user_data.get('target_role', 'professional')} with {user_data.get('experience_years', 'several years')} of experience in {user_data.get('industry', 'the industry')}. Skilled in {user_data.get('technical_skills', 'various technologies')} with a proven track record of delivering results.",
            
            "education": f"{user_data.get('degree', 'Bachelor of Science')}\n{user_data.get('school', 'University Name')}, {user_data.get('grad_year', '2023')}",
            
            "skills": f"Technical Skills: {user_data.get('technical_skills', 'Programming, Software Development')}\nSoft Skills: {user_data.get('soft_skills', 'Communication, Leadership, Problem-solving')}"
        }
        
        return fallback_templates.get(section_type, "Content not available")
    
    if not AOAI_KEY or not AOAI_ENDPOINT:
        return f"Azure OpenAI credentials not configured. Please check your .env file."
    
    try:
        # Handle multiple experiences for AI generation
        if section_type == "experience":
            # Check for experiences array first
            if user_data.get('experiences'):
                experiences_text = ""
                for exp in user_data['experiences']:
                    if exp.get('job_title') or exp.get('company'):
                        experiences_text += f"Job Title: {exp.get('job_title', 'Professional')}\n"
                        experiences_text += f"Company: {exp.get('company', 'Company Name')}\n"
                        experiences_text += f"Duration: {exp.get('duration', '2020-2023')}\n"
                        experiences_text += f"Responsibilities: {exp.get('responsibilities', 'Various responsibilities')}\n"
                        experiences_text += f"Achievements: {exp.get('achievements', 'Notable accomplishments')}\n\n"
                
                prompt = f"""Create professional work experience entries based on this information:
{experiences_text}

Format as professional work experience entries with bullet points highlighting key responsibilities and achievements. Use action verbs and quantify results where possible. Separate each position clearly with proper spacing."""
                
                response = client.ChatCompletion.create(
                    engine=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,  # Increased for multiple experiences
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            else:
                # Use single experience format
                prompt = f"""Create professional work experience entries based on this information:
- Job Title: {user_data.get('job_title', 'Professional')}
- Company: {user_data.get('company', 'Company Name')}
- Duration: {user_data.get('duration', '2020-2023')}
- Responsibilities: {user_data.get('responsibilities', 'Various responsibilities')}
- Achievements: {user_data.get('achievements', 'Notable accomplishments')}

Format as a professional work experience entry with bullet points highlighting key responsibilities and achievements. Use action verbs and quantify results where possible."""
                
                response = client.ChatCompletion.create(
                    engine=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
        
        # Rest of the existing prompts for other sections...
        prompts = {
            "summary": f"""Create a professional resume summary/objective for someone with the following background:
- Name: {user_data.get('name', 'Professional')}
- Job Title/Target Role: {user_data.get('target_role', 'Professional')}
- Years of Experience: {user_data.get('experience_years', 'Entry level')}
- Key Skills: {user_data.get('technical_skills', 'Various skills')}
- Industry: {user_data.get('industry', 'General')}

Write a compelling 2-3 sentence professional summary that highlights their strengths and career goals.""",
            
            "education": f"""Create an education section based on:
- Degree: {user_data.get('degree', 'Degree')}
- School: {user_data.get('school', 'University')}
- Graduation Year: {user_data.get('grad_year', '2023')}
- GPA: {user_data.get('gpa', '')}
- Relevant Coursework: {user_data.get('coursework', '')}

Format as a clean education entry suitable for a resume.""",
            
            "skills": f"""Organize and format these skills into professional categories:
- Technical Skills: {user_data.get('technical_skills', '')}
- Soft Skills: {user_data.get('soft_skills', '')}
- Industry Skills: {user_data.get('industry_skills', '')}
- Languages: {user_data.get('languages', '')}

Format as a well-organized skills section with appropriate categories and bullet points."""
        }

        # Use the older OpenAI library syntax
        response = client.ChatCompletion.create(
            engine=MODEL_NAME,
            messages=[{"role": "user", "content": prompts.get(section_type, prompts["summary"])}],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error generating {section_type}: {e}")
        # Return fallback content with better error handling
        if section_type == "experience":
            if user_data.get('experiences'):
                fallback_text = ""
                for exp in user_data['experiences']:
                    if exp.get('job_title') or exp.get('company'):
                        fallback_text += f"{exp.get('job_title', 'Professional')}\n"
                        fallback_text += f"{exp.get('company', 'Company')} | {exp.get('duration', '2020-2023')}\n"
                        fallback_text += f"• {exp.get('responsibilities', 'Various responsibilities')}\n"
                        fallback_text += f"• {exp.get('achievements', 'Notable achievements')}\n\n"
                return fallback_text
            else:
                return f"{user_data.get('job_title', 'Professional')}\n{user_data.get('company', 'Company')} | {user_data.get('duration', '2020-2023')}\n• {user_data.get('responsibilities', 'Various responsibilities')}\n• {user_data.get('achievements', 'Notable achievements')}"
        
        fallback_templates = {
            "summary": f"Experienced {user_data.get('target_role', 'professional')} with strong background in {user_data.get('industry', 'the industry')}.",
            "education": f"{user_data.get('degree', 'Degree')} from {user_data.get('school', 'University')}",
            "skills": f"Technical Skills: {user_data.get('technical_skills', 'Various skills')}"
        }
        return fallback_templates.get(section_type, "Content not available")
    
def generate_full_resume(user_data):
    """
    Generate a complete resume using user data
    
    Args:
        user_data (dict): Complete user information
        
    Returns:
        dict: Complete resume sections
    """
    
    # Debug: Print the user_data to see what we're receiving
    print("DEBUG: Full user_data received:", user_data)
    
    # If no experiences array exists, create one from the single experience fields
    if not user_data.get('experiences') and (user_data.get('job_title') or user_data.get('company')):
        user_data['experiences'] = [{
            'job_title': user_data.get('job_title', ''),
            'company': user_data.get('company', ''),
            'duration': user_data.get('duration', ''),
            'responsibilities': user_data.get('responsibilities', ''),
            'achievements': user_data.get('achievements', '')
        }]
    
    print("DEBUG: Experiences array:", user_data.get('experiences', []))
    
    resume = {
        "personal_info": {
            "name": user_data.get('name', ''),
            "email": user_data.get('email', ''),
            "phone": user_data.get('phone', ''),
            "address": user_data.get('address', ''),
            "linkedin": user_data.get('linkedin', '')
        },
        "summary": generate_resume_section("summary", user_data),
        "experience": generate_resume_section("experience", user_data),  # This will now use the experiences array
        "education": generate_resume_section("education", user_data),
        "skills": generate_resume_section("skills", user_data)
    }
    
    print("DEBUG: Generated experience section:", resume.get('experience', 'No experience'))
    
    return resume

def generate_resume_pdf(resume_data):
    """
    Generate a compact, single-page PDF resume
    
    Args:
        resume_data (dict): Complete resume data
        
    Returns:
        bytes: PDF file content as bytes
    """
    
    # Create a BytesIO buffer to hold the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document with tighter margins for single page
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        topMargin=0.5*inch, 
        bottomMargin=0.4*inch,
        leftMargin=0.6*inch,
        rightMargin=0.6*inch
    )
    
    # Import additional reportlab components for styling
    from reportlab.lib.colors import HexColor, black, white
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors
    
    # Define modern color palette
    primary_color = HexColor('#0071e3')      # Apple Blue
    secondary_color = HexColor('#1d1d1f')    # Dark Gray
    accent_color = HexColor('#86868b')       # Light Gray
    background_color = HexColor('#f8f8f8')   # Very Light Gray (lighter for compactness)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Compact Times New Roman styles
    name_style = ParagraphStyle(
        'CompactName',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=0.05*inch,
        alignment=TA_CENTER,
        textColor=secondary_color,
        fontName='Times-Bold',
        letterSpacing=0.5
    )
    
    contact_style = ParagraphStyle(
        'CompactContact',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=0.15*inch,
        alignment=TA_CENTER,
        textColor=accent_color,
        fontName='Times-Roman'
    )
    
    section_heading_style = ParagraphStyle(
        'CompactSectionHeading',
        parent=styles['Heading2'],
        fontSize=11,  # Made smaller for single page
        spaceBefore=0.08*inch,  # Reduced spacing
        spaceAfter=0.04*inch,   # Reduced spacing
        textColor=primary_color,
        fontName='Times-Bold',
        letterSpacing=0.3,
        borderWidth=0,
        borderPadding=0,
        leftIndent=0,
        backColor=None
    )
    
    content_style = ParagraphStyle(
        'CompactContent',
        parent=styles['Normal'],
        fontSize=9,  # Made smaller for single page
        spaceAfter=0.03*inch,  # Minimal spacing
        leftIndent=0.1*inch,
        textColor=secondary_color,
        fontName='Times-Roman',
        leading=10,  # Tight line spacing
        alignment=TA_LEFT
    )
    
    # Minimal accent line style
    line_style = ParagraphStyle(
        'MinimalLine',
        parent=styles['Normal'],
        fontSize=1,
        spaceAfter=0.02*inch,
        textColor=primary_color,
        backColor=primary_color
    )
    
    # Build the content
    story = []
    
    # Personal Information
    personal = resume_data.get('personal_info', {})
    
    # Name with compact styling
    if personal.get('name'):
        story.append(Paragraph(personal['name'].upper(), name_style))
    
    # Contact info in a more compact format
    contact_parts = []
    if personal.get('email'):
        contact_parts.append(personal['email'])
    if personal.get('phone'):
        contact_parts.append(personal['phone'])
    if personal.get('address'):
        contact_parts.append(personal['address'])
    if personal.get('linkedin'):
        contact_parts.append(f"LinkedIn: {personal['linkedin']}")
    
    if contact_parts:
        contact_text = " | ".join(contact_parts)
        story.append(Paragraph(contact_text, contact_style))
    
    # Add a minimal divider line
    story.append(Paragraph("_" * 60, line_style))
    
    # Professional Summary
    if resume_data.get('summary'):
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading_style))
        story.append(Paragraph(resume_data['summary'], content_style))
        story.append(Spacer(1, 0.03*inch))
    
    # Work Experience - PROPERLY HANDLE MULTIPLE EXPERIENCES
    if resume_data.get('experience'):
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading_style))
        
        # Parse the experience text to separate multiple experiences
        experience_text = resume_data['experience']
        
        # Split experience by double newlines (which separate different jobs)
        experience_blocks = experience_text.split('\n\n\n')  # Triple newline separates jobs
        if len(experience_blocks) == 1:
            # Try double newline if triple doesn't work
            experience_blocks = experience_text.split('\n\n')
        
        # Process each experience block separately
        for i, block in enumerate(experience_blocks):
            if block.strip():  # Only process non-empty blocks
                lines = block.strip().split('\n')
                formatted_block = ""
                
                for line in lines:
                    line = line.strip()
                    if line:
                        # Check if this is a job title line (usually the first non-bullet line)
                        if not line.startswith('•') and not '|' in line and len(lines) > 1 and line == lines[0]:
                            # This is likely a job title - make it bold
                            formatted_block += f"<b>{line}</b><br/>"
                        elif '|' in line and not line.startswith('•'):
                            # This is likely company | duration line
                            formatted_block += f"{line}<br/>"
                        elif line.startswith('•'):
                            # This is a bullet point
                            formatted_block += f"{line}<br/>"
                        else:
                            # Regular line
                            formatted_block += f"{line}<br/>"
                
                # Add the formatted block
                story.append(Paragraph(formatted_block, content_style))
                
                # Add small spacing between different experiences (except the last one)
                if i < len(experience_blocks) - 1:
                    story.append(Spacer(1, 0.02*inch))
        
        story.append(Spacer(1, 0.03*inch))
    
    # Education - compact format
    if resume_data.get('education'):
        story.append(Paragraph("EDUCATION", section_heading_style))
        
        education_text = resume_data['education'].replace('\n', '<br/>')
        story.append(Paragraph(education_text, content_style))
        story.append(Spacer(1, 0.03*inch))
    
    # Skills - most compact format
    if resume_data.get('skills'):
        story.append(Paragraph("CORE COMPETENCIES", section_heading_style))
        
        # Parse and format skills compactly
        skills_text = resume_data['skills']
        skills_formatted = skills_text.replace('\n\n', '<br/>')
        skills_formatted = skills_formatted.replace('\n', '<br/>')
        skills_formatted = skills_formatted.replace('Technical Skills:', '<b>Technical Skills:</b>')
        skills_formatted = skills_formatted.replace('Soft Skills:', '<b>Soft Skills:</b>')
        skills_formatted = skills_formatted.replace('Industry Skills:', '<b>Industry Skills:</b>')
        skills_formatted = skills_formatted.replace('Languages:', '<b>Languages:</b>')
        
        story.append(Paragraph(skills_formatted, content_style))
    
    # Minimal footer
    story.append(Spacer(1, 0.05*inch))
    footer_style = ParagraphStyle(
        'CompactFooter',
        parent=styles['Normal'],
        fontSize=7,
        alignment=TA_CENTER,
        textColor=accent_color,
        fontName='Times-Italic'
    )
    story.append(Paragraph("Generated by NextStep AI Resume Builder", footer_style))
    
    # Build the PDF with compact styling
    doc.build(story)
    
    # Get the PDF content
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content

