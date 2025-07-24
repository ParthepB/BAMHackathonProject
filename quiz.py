"""
Career Quiz Backend Logic
Handles quiz processing, scoring, and recommendations
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class CareerRecommendation:
    title: str
    score: int
    description: str
    reasons: List[str]
    salary_range: str = ""
    growth_outlook: str = ""
    required_skills: List[str] = None

class CareerQuizProcessor:
    def __init__(self):
        self.career_profiles = self._initialize_career_profiles()
        self.scoring_weights = {
            'medical': {
                'stress_tolerance': 0.25,
                'continuous_learning': 0.20,
                'helping_others': 0.30,
                'emotional_resilience': 0.15,
                'schedule_flexibility': 0.10
            },
            'tech': {
                'problem_solving': 0.30,
                'tech_learning': 0.25,
                'work_style': 0.20,
                'debugging_skills': 0.15,
                'innovation_drive': 0.10
            },
            'business': {
                'decision_making': 0.25,
                'networking': 0.20,
                'financial_motivation': 0.20,
                'competition_comfort': 0.20,
                'risk_tolerance': 0.15
            },
            'education': {
                'teaching_passion': 0.30,
                'patience': 0.25,
                'motivation_skills': 0.20,
                'public_speaking': 0.15,
                'impact_focus': 0.10
            },
            'arts': {
                'creative_expression': 0.30,
                'criticism_handling': 0.20,
                'income_stability': 0.15,
                'self_promotion': 0.20,
                'artistic_freedom': 0.15
            },
            'other': {
                'environment_preference': 0.20,
                'work_life_balance': 0.25,
                'impact_type': 0.20,
                'skill_application': 0.20,
                'motivation_source': 0.15
            }
        }

    def _initialize_career_profiles(self) -> Dict:
        return {
            'medical': {
                'doctor': {
                    'title': 'Medical Doctor (Physician)',
                    'description': 'Diagnose and treat illnesses, injuries, and health conditions to improve patient outcomes.',
                    'base_score_requirements': {'stress_tolerance': 4, 'helping_others': 4, 'continuous_learning': 4},
                    'salary_range': '$200,000 - $400,000+',
                    'growth_outlook': 'Excellent (7% growth)',
                    'required_skills': ['Medical knowledge', 'Critical thinking', 'Communication', 'Empathy', 'Decision-making']
                },
                'nurse': {
                    'title': 'Registered Nurse',
                    'description': 'Provide direct patient care, support doctors, and advocate for patient health and safety.',
                    'base_score_requirements': {'helping_others': 4, 'emotional_resilience': 3, 'schedule_flexibility': 3},
                    'salary_range': '$75,000 - $120,000',
                    'growth_outlook': 'Excellent (9% growth)',
                    'required_skills': ['Patient care', 'Medical procedures', 'Communication', 'Compassion', 'Attention to detail']
                },
                'medical_researcher': {
                    'title': 'Medical Researcher',
                    'description': 'Conduct research to advance medical knowledge and develop new treatments and therapies.',
                    'base_score_requirements': {'continuous_learning': 5, 'problem_solving': 4, 'helping_others': 3},
                    'salary_range': '$85,000 - $150,000',
                    'growth_outlook': 'Good (6% growth)',
                    'required_skills': ['Research methodology', 'Data analysis', 'Scientific writing', 'Laboratory techniques', 'Critical thinking']
                }
            },
            'tech': {
                'software_engineer': {
                    'title': 'Software Engineer',
                    'description': 'Design, develop, and maintain software applications and systems to solve complex problems.',
                    'base_score_requirements': {'problem_solving': 4, 'tech_learning': 4, 'debugging_skills': 4},
                    'salary_range': '$90,000 - $180,000',
                    'growth_outlook': 'Excellent (13% growth)',
                    'required_skills': ['Programming languages', 'System design', 'Problem solving', 'Debugging', 'Version control']
                },
                'data_scientist': {
                    'title': 'Data Scientist',
                    'description': 'Analyze complex data to extract insights and build predictive models for business decisions.',
                    'base_score_requirements': {'problem_solving': 5, 'tech_learning': 4, 'innovation_drive': 4},
                    'salary_range': '$100,000 - $200,000',
                    'growth_outlook': 'Excellent (35% growth)',
                    'required_skills': ['Statistics', 'Machine learning', 'Python/R', 'Data visualization', 'Business acumen']
                },
                'cybersecurity_specialist': {
                    'title': 'Cybersecurity Specialist',
                    'description': 'Protect organizations from cyber threats and ensure data security and privacy.',
                    'base_score_requirements': {'problem_solving': 4, 'tech_learning': 4, 'debugging_skills': 4},
                    'salary_range': '$95,000 - $170,000',
                    'growth_outlook': 'Excellent (31% growth)',
                    'required_skills': ['Network security', 'Risk assessment', 'Incident response', 'Ethical hacking', 'Compliance']
                }
            },
            'business': {
                'management_consultant': {
                    'title': 'Management Consultant',
                    'description': 'Help organizations improve performance and efficiency through strategic analysis and recommendations.',
                    'base_score_requirements': {'decision_making': 4, 'networking': 4, 'competition_comfort': 4},
                    'salary_range': '$85,000 - $200,000',
                    'growth_outlook': 'Good (11% growth)',
                    'required_skills': ['Strategic thinking', 'Data analysis', 'Communication', 'Project management', 'Business acumen']
                },
                'financial_analyst': {
                    'title': 'Financial Analyst',
                    'description': 'Evaluate investment opportunities and provide financial guidance to businesses and individuals.',
                    'base_score_requirements': {'financial_motivation': 4, 'decision_making': 4, 'risk_tolerance': 3},
                    'salary_range': '$70,000 - $130,000',
                    'growth_outlook': 'Good (6% growth)',
                    'required_skills': ['Financial modeling', 'Data analysis', 'Excel proficiency', 'Market research', 'Communication']
                },
                'entrepreneur': {
                    'title': 'Entrepreneur/Business Owner',
                    'description': 'Start and manage your own business ventures, taking calculated risks to create value.',
                    'base_score_requirements': {'risk_tolerance': 5, 'decision_making': 4, 'competition_comfort': 4},
                    'salary_range': 'Variable ($0 - $1M+)',
                    'growth_outlook': 'Depends on venture',
                    'required_skills': ['Leadership', 'Risk management', 'Networking', 'Innovation', 'Persistence']
                }
            },
            'education': {
                'teacher': {
                    'title': 'K-12 Teacher',
                    'description': 'Educate and inspire students in elementary, middle, or high school settings.',
                    'base_score_requirements': {'teaching_passion': 4, 'patience': 4, 'motivation_skills': 4},
                    'salary_range': '$40,000 - $80,000',
                    'growth_outlook': 'Average (4% growth)',
                    'required_skills': ['Curriculum development', 'Classroom management', 'Communication', 'Patience', 'Creativity']
                },
                'professor': {
                    'title': 'College Professor',
                    'description': 'Teach at the university level while conducting research in your field of expertise.',
                    'base_score_requirements': {'teaching_passion': 4, 'continuous_learning': 5, 'public_speaking': 4},
                    'salary_range': '$60,000 - $150,000',
                    'growth_outlook': 'Good (9% growth)',
                    'required_skills': ['Subject expertise', 'Research skills', 'Public speaking', 'Writing', 'Critical thinking']
                },
                'corporate_trainer': {
                    'title': 'Corporate Trainer',
                    'description': 'Design and deliver training programs to help employees develop professional skills.',
                    'base_score_requirements': {'teaching_passion': 4, 'public_speaking': 4, 'motivation_skills': 4},
                    'salary_range': '$55,000 - $100,000',
                    'growth_outlook': 'Good (11% growth)',
                    'required_skills': ['Training design', 'Presentation skills', 'Adult learning', 'Communication', 'Assessment']
                }
            },
            'arts': {
                'graphic_designer': {
                    'title': 'Graphic Designer',
                    'description': 'Create visual content for digital and print media to communicate messages effectively.',
                    'base_score_requirements': {'creative_expression': 4, 'artistic_freedom': 3, 'criticism_handling': 3},
                    'salary_range': '$45,000 - $85,000',
                    'growth_outlook': 'Average (3% growth)',
                    'required_skills': ['Design software', 'Typography', 'Color theory', 'Creativity', 'Client communication']
                },
                'content_creator': {
                    'title': 'Content Creator/Influencer',
                    'description': 'Create engaging content across digital platforms to build audiences and partnerships.',
                    'base_score_requirements': {'creative_expression': 4, 'self_promotion': 4, 'income_stability': 2},
                    'salary_range': '$30,000 - $200,000+',
                    'growth_outlook': 'Excellent (varies by niche)',
                    'required_skills': ['Content creation', 'Social media', 'Video editing', 'Marketing', 'Personal branding']
                },
                'art_director': {
                    'title': 'Art Director',
                    'description': 'Lead creative teams and oversee visual concepts for advertising, media, and marketing campaigns.',
                    'base_score_requirements': {'creative_expression': 4, 'leadership': 4, 'criticism_handling': 4},
                    'salary_range': '$70,000 - $140,000',
                    'growth_outlook': 'Average (2% growth)',
                    'required_skills': ['Creative leadership', 'Project management', 'Design expertise', 'Team collaboration', 'Strategic thinking']
                }
            },
            'other': {
                'environmental_scientist': {
                    'title': 'Environmental Scientist',
                    'description': 'Study environmental problems and develop solutions to protect human health and the environment.',
                    'base_score_requirements': {'impact_type': 5, 'environment_preference': 4, 'motivation_source': 4},
                    'salary_range': '$65,000 - $120,000',
                    'growth_outlook': 'Good (8% growth)',
                    'required_skills': ['Environmental science', 'Data analysis', 'Field research', 'Report writing', 'Problem solving']
                },
                'social_worker': {
                    'title': 'Social Worker',
                    'description': 'Help individuals, families, and communities overcome challenges and improve their well-being.',
                    'base_score_requirements': {'motivation_source': 5, 'impact_type': 4, 'work_life_balance': 3},
                    'salary_range': '$45,000 - $80,000',
                    'growth_outlook': 'Good (12% growth)',
                    'required_skills': ['Counseling', 'Case management', 'Communication', 'Empathy', 'Crisis intervention']
                },
                'project_manager': {
                    'title': 'Project Manager',
                    'description': 'Plan, execute, and oversee projects across various industries to achieve specific goals.',
                    'base_score_requirements': {'skill_application': 4, 'work_life_balance': 3, 'motivation_source': 3},
                    'salary_range': '$75,000 - $130,000',
                    'growth_outlook': 'Good (7% growth)',
                    'required_skills': ['Project planning', 'Leadership', 'Communication', 'Risk management', 'Time management']
                }
            }
        }

    def process_quiz(self, career_type: str, answers: Dict) -> List[CareerRecommendation]:
        """
        Process quiz answers and return top 3 career recommendations
        """
        if career_type not in self.career_profiles:
            return self._get_default_recommendations()

        # Calculate scores for each career in the selected category
        career_scores = []
        careers = self.career_profiles[career_type]
        weights = self.scoring_weights.get(career_type, {})

        for career_key, career_data in careers.items():
            score = self._calculate_career_score(answers, career_data, weights, career_type)
            
            recommendation = CareerRecommendation(
                title=career_data['title'],
                score=min(100, max(0, score)),  # Ensure score is between 0-100
                description=career_data['description'],
                reasons=self._generate_reasons(answers, career_data, career_type),
                salary_range=career_data.get('salary_range', 'Varies'),
                growth_outlook=career_data.get('growth_outlook', 'Average'),
                required_skills=career_data.get('required_skills', [])
            )
            
            career_scores.append(recommendation)

        # Sort by score and return top 3
        career_scores.sort(key=lambda x: x.score, reverse=True)
        return career_scores[:3]

    def _calculate_career_score(self, answers: Dict, career_data: Dict, weights: Dict, career_type: str) -> int:
        """
        Calculate compatibility score for a specific career
        """
        base_score = 60  # Starting score
        
        # Convert answers dict to list of values
        answer_values = []
        for i in range(5):  # We have 5 questions per career type
            if str(i) in answers:
                answer_values.append(answers[str(i)]['value'])
            else:
                answer_values.append(3)  # Default neutral score

        # Apply career-specific scoring logic
        if career_type == 'medical':
            # Higher weight on stress tolerance, helping others, and continuous learning
            score_factors = {
                0: answer_values[0] * 8,  # stress tolerance
                1: answer_values[1] * 6,  # continuous learning
                2: answer_values[2] * 10, # helping others (most important)
                3: answer_values[3] * 5,  # emotional resilience
                4: answer_values[4] * 3   # schedule flexibility
            }
        elif career_type == 'tech':
            # Higher weight on problem solving and tech learning
            score_factors = {
                0: answer_values[0] * 10, # problem solving (most important)
                1: answer_values[1] * 8,  # tech learning
                2: answer_values[2] * 4,  # work style
                3: answer_values[3] * 6,  # debugging
                4: answer_values[4] * 4   # innovation
            }
        elif career_type == 'business':
            # Balanced across all business skills
            score_factors = {
                0: answer_values[0] * 7,  # decision making
                1: answer_values[1] * 6,  # networking
                2: answer_values[2] * 6,  # financial motivation
                3: answer_values[3] * 6,  # competition
                4: answer_values[4] * 7   # risk tolerance
            }
        elif career_type == 'education':
            # Higher weight on teaching passion and patience
            score_factors = {
                0: answer_values[0] * 10, # teaching passion (most important)
                1: answer_values[1] * 8,  # patience
                2: answer_values[2] * 6,  # motivation skills
                3: answer_values[3] * 5,  # public speaking
                4: answer_values[4] * 3   # impact focus
            }
        elif career_type == 'arts':
            # Higher weight on creative expression and artistic freedom
            score_factors = {
                0: answer_values[0] * 10, # creative expression (most important)
                1: answer_values[1] * 5,  # criticism handling
                2: answer_values[2] * 3,  # income stability (reverse scored)
                3: answer_values[3] * 6,  # self promotion
                4: answer_values[4] * 8   # artistic freedom
            }
        else:  # other
            # Balanced general approach
            score_factors = {
                0: answer_values[0] * 5,  # environment preference
                1: answer_values[1] * 7,  # work-life balance
                2: answer_values[2] * 6,  # impact type
                3: answer_values[3] * 6,  # skill application
                4: answer_values[4] * 6   # motivation
            }

        # Calculate total score
        total_factor_score = sum(score_factors.values())
        
        # Normalize to 0-100 scale
        max_possible_score = 5 * sum([8, 6, 10, 5, 3])  # Using medical weights as reference
        normalized_score = (total_factor_score / max_possible_score) * 100
        
        return int(normalized_score)

    def _generate_reasons(self, answers: Dict, career_data: Dict, career_type: str) -> List[str]:
        """
        Generate personalized reasons why this career fits the user
        """
        reasons = []
        
        # Convert answers to list for easier access
        answer_values = []
        for i in range(5):
            if str(i) in answers:
                answer_values.append(answers[str(i)]['value'])
            else:
                answer_values.append(3)

        # Career-specific reason generation
        if career_type == 'medical':
            if answer_values[0] >= 4:
                reasons.append("You handle high-stress situations well, which is crucial in medical settings")
            if answer_values[1] >= 4:
                reasons.append("Your commitment to continuous learning aligns with the evolving medical field")
            if answer_values[2] >= 4:
                reasons.append("Your strong desire to help others directly matches the core mission of healthcare")
            if answer_values[3] >= 4:
                reasons.append("You demonstrate emotional resilience needed for patient care")
                
        elif career_type == 'tech':
            if answer_values[0] >= 4:
                reasons.append("Your love for solving complex problems is perfect for technical challenges")
            if answer_values[1] >= 4:
                reasons.append("Your enthusiasm for learning new technologies will keep you current in this fast-evolving field")
            if answer_values[3] >= 4:
                reasons.append("Your debugging and troubleshooting skills are highly valued in tech roles")
            if answer_values[4] >= 4:
                reasons.append("Your drive for innovation aligns with the creative aspects of technology work")
                
        elif career_type == 'business':
            if answer_values[0] >= 4:
                reasons.append("Your comfort with decision-making under pressure is essential for business leadership")
            if answer_values[1] >= 4:
                reasons.append("Your networking skills will help you build valuable professional relationships")
            if answer_values[3] >= 4:
                reasons.append("Your competitive nature will drive success in business environments")
            if answer_values[4] >= 4:
                reasons.append("Your willingness to take calculated risks is crucial for business growth")
                
        elif career_type == 'education':
            if answer_values[0] >= 4:
                reasons.append("Your passion for explaining concepts makes you a natural educator")
            if answer_values[1] >= 4:
                reasons.append("Your patience with different learning speeds is invaluable for teaching")
            if answer_values[2] >= 4:
                reasons.append("Your ability to inspire others is a key trait of effective educators")
            if answer_values[4] >= 4:
                reasons.append("Your focus on making a positive impact aligns with education's mission")
                
        elif career_type == 'arts':
            if answer_values[0] >= 4:
                reasons.append("Your need for creative expression is fundamental to artistic careers")
            if answer_values[1] >= 4:
                reasons.append("Your ability to handle criticism constructively will help you grow as an artist")
            if answer_values[3] >= 4:
                reasons.append("Your comfort with self-promotion is important for artistic success")
            if answer_values[4] >= 4:
                reasons.append("Your desire for artistic freedom aligns with creative career paths")
                
        else:  # other
            if answer_values[1] >= 4:
                reasons.append("Your emphasis on work-life balance suggests careers with flexible arrangements")
            if answer_values[2] >= 4:
                reasons.append("Your desire to make a specific type of impact guides suitable career choices")
            if answer_values[4] >= 4:
                reasons.append("Your motivation sources align well with these career paths")

        # Ensure we have at least 2 reasons
        if len(reasons) < 2:
            reasons.extend([
                "Your personality profile shows strong compatibility with this field",
                "Your skills and interests align well with the typical requirements"
            ])

        return reasons[:4]  # Return max 4 reasons

    def _get_default_recommendations(self) -> List[CareerRecommendation]:
        """
        Return default recommendations if career type is not found
        """
        return [
            CareerRecommendation(
                title="Career Exploration Specialist",
                score=75,
                description="Help others discover their ideal career paths through counseling and assessment.",
                reasons=[
                    "Your interest in career development shows aptitude for this field",
                    "You understand the importance of finding the right career fit",
                    "Your willingness to explore shows good self-awareness"
                ]
            ),
            CareerRecommendation(
                title="General Project Coordinator",
                score=70,
                description="Manage projects across various industries while exploring different career options.",
                reasons=[
                    "This role offers exposure to multiple industries",
                    "You can develop transferable skills",
                    "It provides flexibility to explore interests"
                ]
            ),
            CareerRecommendation(
                title="Research Assistant",
                score=65,
                description="Support research activities while gaining exposure to various fields and methodologies.",
                reasons=[
                    "Research skills are valuable across many careers",
                    "You can explore different subject areas",
                    "It builds analytical and critical thinking skills"
                ]
            )
        ]

def process_career_quiz(career_type: str, answers: Dict) -> Dict:
    """
    Main function to process career quiz and return recommendations
    """
    processor = CareerQuizProcessor()
    recommendations = processor.process_quiz(career_type, answers)
    
    # Convert to JSON-serializable format
    result = {
        'recommendations': [
            {
                'title': rec.title,
                'score': rec.score,
                'description': rec.description,
                'reasons': rec.reasons,
                'salary_range': rec.salary_range,
                'growth_outlook': rec.growth_outlook,
                'required_skills': rec.required_skills or []
            }
            for rec in recommendations
        ],
        'career_type': career_type,
        'total_questions': len(answers)
    }
    
    return result

# Example usage and testing
if __name__ == "__main__":
    # Test the system
    sample_answers = {
        '0': {'value': 5, 'text': 'Very comfortable, I thrive under pressure'},
        '1': {'value': 4, 'text': 'I enjoy learning new things'},
        '2': {'value': 5, 'text': 'Extremely important, it\'s my passion'},
        '3': {'value': 4, 'text': 'It\'s difficult but I can manage'},
        '4': {'value': 3, 'text': 'It\'s manageable'}
    }
    
    result = process_career_quiz('medical', sample_answers)
    print(json.dumps(result, indent=2))
