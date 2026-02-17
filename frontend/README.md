# Frontend - Internship Scam Detector

A complete multi-page website for detecting fake internship postings using AI.

## 📄 Pages

### 1. Home Page (`home.html`)
- Hero section with call-to-action
- Features overview
- Common red flags
- Statistics

### 2. About Page (`about.html`)
- Project mission and technology
- How it works
- Dataset information
- FAQ section
- Technology stack

### 3. Awareness Page (`awareness.html`)
- Safety tips and protection guidelines
- Major red flags with severity levels
- Real scam examples vs legitimate postings
- What to do if you encounter a scam
- Scam statistics

### 4. Analyzer Page (`analyzer.html`)
- AI-powered job posting analysis
- Multiple input options:
  - Job posting text
  - LinkedIn profile URL
  - Company website URL
  - Screenshot upload
- Real-time ML predictions
- Detailed risk breakdown

## 🎨 Design Features

- Modern gradient design
- Responsive layout (mobile-friendly)
- Smooth animations
- Color-coded results (green/yellow/red)
- Professional navigation
- Consistent branding

## 🚀 Setup

No build process needed! Just open any HTML file in your browser.

### Option 1: Direct File
```bash
# Windows
start home.html

# Mac
open home.html

# Linux
xdg-open home.html
```

### Option 2: Local Server
```bash
# Python 3
python -m http.server 3000

# Then visit: http://localhost:3000/home.html
```

## 🔗 Backend Integration

The analyzer page connects to the backend API at `http://localhost:8000`

Make sure the backend is running:
```bash
cd ../backend
uvicorn app.main:app --reload
```

## 📁 File Structure

```
frontend/
├── home.html          # Landing page
├── about.html         # About the project
├── awareness.html     # Safety tips and education
├── analyzer.html      # AI analysis tool
├── styles.css         # Shared styles
└── README.md          # This file
```

## 🎯 Navigation Flow

```
Home → About / Awareness / Analyzer
  ↓
About → FAQ / Technology Details
  ↓
Awareness → Safety Tips / Report Scam
  ↓
Analyzer → Real-time Analysis
```

## ✨ Key Features

1. **Quick Test Examples** - Pre-loaded scam and legitimate examples
2. **ML Model Display** - Shows AI confidence and predictions
3. **Multi-Factor Analysis** - Text, website, LinkedIn, screenshot checks
4. **Educational Content** - Comprehensive awareness and safety tips
5. **Responsive Design** - Works on desktop, tablet, and mobile

## 🎨 Color Scheme

- Primary: `#667eea` (Purple-blue)
- Secondary: `#764ba2` (Deep purple)
- Success: `#28a745` (Green)
- Warning: `#ffc107` (Yellow)
- Danger: `#dc3545` (Red)

## 📱 Responsive Breakpoints

- Desktop: > 768px
- Tablet/Mobile: ≤ 768px

## 🔧 Customization

To customize the design:
1. Edit `styles.css` for global styles
2. Edit inline styles in each HTML file for page-specific changes
3. Update colors in the CSS variables

## 🌐 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Opera

## 📝 Notes

- All pages are standalone HTML files
- No JavaScript framework required
- Vanilla JavaScript for interactivity
- CSS Grid and Flexbox for layouts
- No external dependencies except backend API

Enjoy protecting job seekers from scams! 🛡️
