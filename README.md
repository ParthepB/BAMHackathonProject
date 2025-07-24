# 🚀 NextStep - Your AI-Powered Career Development Platform

![NextStep Logo](static/images/NextStep.png)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

NextStep is a comprehensive AI-powered career development platform designed to help professionals at every stage of their career journey. From career discovery to resume optimization, NextStep provides intelligent tools and personalized guidance to accelerate your professional growth.

### 🎯 Mission
Empowering professionals with AI-driven career tools that provide personalized insights, professional content generation, and intelligent career guidance.

## ✨ Features

### 🧭 Career Quiz
- **Comprehensive Assessment**: 30+ questions across 6 career categories
- **Intelligent Scoring**: Advanced algorithm analyzes responses
- **Personalized Recommendations**: Get matched with ideal career paths
- **Industry Insights**: Detailed information about recommended careers

### 🤖 AI Resume Maker
- **Smart Content Generation**: Azure OpenAI-powered resume creation
- **Professional Templates**: Industry-standard formatting
- **Fallback System**: Works even when AI is unavailable
- **Real-time Preview**: See your resume as you build it
- **Multiple Export Options**: Download or copy to clipboard

### 📊 Resume Grader *(Coming Soon)*
- Automated resume analysis and scoring
- ATS compatibility checking
- Improvement suggestions

### 🎤 Mock Interview Bot *(Coming Soon)*
- AI-powered interview practice
- Industry-specific questions
- Performance feedback and tips

### 🎨 Modern UI/UX
- **Apple-inspired Design**: Clean, minimalist interface
- **Responsive Layout**: Works on all devices
- **Smooth Animations**: Engaging scroll effects
- **Intuitive Navigation**: User-friendly interface

## 🛠 Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **AI Integration**: Azure OpenAI (GPT-3.5-turbo)
- **Environment Management**: python-dotenv
- **Language**: Python 3.x

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with Apple-inspired design
- **Authentication**: LocalStorage-based session management
- **Responsive Design**: Mobile-first approach

### AI & APIs
- **Azure OpenAI**: Resume generation and content improvement
- **Custom Algorithms**: Career matching and scoring system
- **RESTful APIs**: JSON-based data exchange

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Git

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ParthepB/BAMHackathonProject.git
   cd BAMHackathonProject
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-05-01-preview
   AZURE_OPENAI_DEPLOYMENT=gpt-35-turbo
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Platform**
   Open your browser and navigate to `http://localhost:5000`

## ⚙️ Configuration

### Azure OpenAI Setup
1. Create an Azure OpenAI resource in the Azure portal
2. Deploy a GPT-3.5-turbo model
3. Copy your API key and endpoint
4. Update the `.env` file with your credentials

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | Yes* |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint URL | Yes* |
| `AZURE_OPENAI_DEPLOYMENT` | Model deployment name | Yes* |

*Required for AI features. The platform includes fallback functionality if AI is unavailable.

## 📖 Usage

### Getting Started
1. **Sign Up/Login**: Create an account or log in to access features
2. **Take the Career Quiz**: Discover your ideal career path
3. **Create Your Resume**: Use AI to generate professional content
4. **Explore Features**: Access additional career development tools

### Career Quiz
- Complete 30 targeted questions
- Receive personalized career recommendations
- View detailed career information and requirements
- Get matched based on your interests and skills

### AI Resume Maker
- Fill out comprehensive form with your information
- Generate AI-powered content for each section
- Preview your resume in real-time
- Download or copy your finished resume

## 🔌 API Endpoints

### Career Quiz
- `GET /career-quiz` - Display career quiz interface
- `POST /submit-quiz` - Process quiz responses and return results

### Resume Generation
- `GET /rmaker` - Display resume maker interface
- `POST /api/generate-resume` - Generate AI-powered resume content

### Navigation
- `GET /` - Home page
- `GET /features` - Features overview
- `GET /about` - About page
- `GET /contact` - Contact information
- `GET /settings` - User settings

## 📁 Project Structure

```
BAMHackathonProject/
├── app.py                 # Main Flask application
├── quiz.py               # Career quiz logic and data
├── rmaker.py             # AI resume generation backend
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in repo)
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
│
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   │   ├── home.css    # Home page styles
│   │   ├── style.css   # Global styles
│   │   └── rmaker.css  # Resume maker styles
│   ├── js/             # JavaScript files
│   │   └── style.js    # Main JavaScript
│   └── images/         # Image assets
│       └── NextStep.png # Logo
│
└── templates/           # HTML templates
    ├── home.html        # Landing page
    ├── features.html    # Features page
    ├── about.html       # About page
    ├── contact.html     # Contact page
    ├── settings.html    # Settings page
    ├── quiz_result.html # Quiz results
    ├── rmaker.html      # Resume maker
    ├── rgrader.html     # Resume grader
    └── mock.html        # Mock interview
```

## 🏗️ Architecture

### Backend Architecture
- **Flask Application**: Lightweight web framework
- **Modular Design**: Separate modules for different features
- **Error Handling**: Comprehensive exception management
- **Fallback Systems**: Graceful degradation when AI is unavailable

### Frontend Architecture
- **Responsive Design**: Mobile-first CSS approach
- **Progressive Enhancement**: Works without JavaScript
- **Modern CSS**: Flexbox, Grid, and CSS custom properties
- **Smooth Animations**: CSS transitions and transforms

### AI Integration
- **Azure OpenAI**: Primary AI service for content generation
- **Fallback Templates**: Static templates when AI is unavailable
- **Error Recovery**: Automatic fallback to templates on AI failure

## 🤝 Contributing

We welcome contributions to NextStep! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with descriptive messages
5. Push to your fork and submit a pull request

### Contribution Guidelines
- Follow Python PEP 8 style guidelines
- Write descriptive commit messages
- Include tests for new features
- Update documentation as needed
- Ensure responsive design compatibility

### Areas for Contribution
- 🐛 Bug fixes and improvements
- ✨ New features and enhancements
- 📚 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Testing and quality assurance

## 📊 Roadmap

### Phase 1 ✅ (Completed)
- [x] Career Quiz system
- [x] AI Resume Maker
- [x] Basic authentication
- [x] Responsive design

### Phase 2 🚧 (In Progress)
- [ ] Resume Grader functionality
- [ ] Mock Interview Bot
- [ ] User profiles and data persistence
- [ ] Advanced analytics

### Phase 3 🎯 (Planned)
- [ ] Job matching system
- [ ] Career path visualization
- [ ] Social features and networking
- [ ] Mobile application

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Development Team**: BAM Hackathon Project Team
- **AI Integration**: Azure OpenAI Implementation
- **UI/UX Design**: Apple-inspired modern interface

## 📞 Support

For support, questions, or feedback:
- 📧 Email: support@nextstep.dev
- 🐛 Issues: [GitHub Issues](https://github.com/ParthepB/BAMHackathonProject/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ParthepB/BAMHackathonProject/discussions)

## 🙏 Acknowledgments

- Azure OpenAI for AI capabilities
- Flask community for the excellent framework
- Open source contributors and libraries
- BAM Hackathon organizers and participants

---

<div align="center">
  <strong>🚀 NextStep - Accelerating Your Career Journey</strong><br>
  Made with ❤️ for professionals worldwide
</div>
