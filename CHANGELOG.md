# Changelog

All notable changes to the Codebase Time Machine project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2024-08-16

### 🚀 Major AI Upgrade

#### GPT-5 Integration
- **Upgraded from GPT-4 to GPT-5**: Enhanced AI capabilities for better code analysis and Q&A responses
- **API Parameter Updates**: Updated to use GPT-5's required parameters (`max_completion_tokens` instead of `max_tokens`)
- **Temperature Optimization**: Adapted to GPT-5's parameter constraints (uses default temperature of 1)
- **Improved Analysis Quality**: Better understanding of complex codebases and architectural patterns

### 🔧 Technical Changes
- **Backend**: Updated OpenAI API calls to GPT-5 compatibility
- **Dependencies**: Updated to `openai>=1.50.0` for GPT-5 support
- **UI Updates**: Updated footer to reflect GPT-5 usage
- **Documentation**: Updated all references from GPT-4 to GPT-5

---

## [2.0.0] - 2024-08-16

### 🚀 Major Features Added

#### Q&A Interface
- **Interactive Q&A System**: Added natural language question interface allowing users to ask questions like "Why was this pattern introduced?" or "Show me how auth evolved"
- **GPT-4 Powered Analysis**: Implemented intelligent commit analysis with evidence-based responses and citation of specific commits
- **Suggested Questions**: Added smart question suggestions based on the topic being analyzed
- **Real-time Q&A**: Users can ask follow-up questions without re-analyzing the repository

#### Advanced Visualizations
- **Code Ownership Charts**: Horizontal bar charts showing commit distribution and lines changed by author
- **File Hotspot Analysis**: Visual identification of frequently changed files (complexity indicators)
- **Development Trends**: Monthly complexity trends showing lines added/deleted and file activity over time
- **Evolution Timeline**: Enhanced timeline showing key development moments and architectural changes

#### Enhanced User Experience
- **Tabbed Interface**: Clean navigation between Summary, Timeline, Q&A, and Insights sections
- **Chart.js Integration**: Professional, responsive data visualizations
- **Mobile-Responsive Design**: Optimized for all screen sizes with collapsible elements
- **Loading States**: Improved UX with proper loading indicators and error handling

### 🔧 Technical Improvements

#### Backend Enhancements
- **New `/qa` Endpoint**: Dedicated API endpoint for custom question processing
- **Enhanced Git Analysis**: Extended GitAnalyzer with author aggregation, hotspot detection, and complexity trending
- **Visualization Data Generation**: Automatic generation of chart-ready data structures
- **Structured Q&A Processing**: Following qa-feature-ui.md template for consistent response formatting

#### Frontend Architecture
- **New React Components**: 
  - `QASection.tsx` - Interactive Q&A interface
  - `OwnershipChart.tsx` - Code ownership visualization
  - `HotspotChart.tsx` - File change frequency charts
  - `ComplexityTrend.tsx` - Development complexity trends
- **Enhanced Type System**: Complete TypeScript interfaces for Q&A and visualization data
- **State Management**: Improved app state handling with tab navigation and data persistence

#### Dependencies
- **Chart.js**: Added `chart.js` and `react-chartjs-2` for professional data visualization
- **Enhanced Python Backend**: Updated FastAPI integration with new pydantic models

### 🐛 Bug Fixes
- Fixed port configuration for local development (backend now runs on port 5002)
- Improved error handling for git analysis and GPT processing
- Enhanced CORS configuration for seamless frontend-backend communication

### 📚 Documentation
- Updated CLAUDE.md with new development commands and architecture details
- Enhanced README.md with feature overview and usage instructions
- Added comprehensive inline documentation for new components

### 🎯 API Changes
- **`/analyze` endpoint**: Now returns additional `qa_data` and `visualizations` fields
- **New `/qa` endpoint**: Accepts `{question, repo_url, topic}` and returns structured Q&A responses
- **Enhanced response schemas**: Added support for ownership data, hotspots, and complexity trends

---

## [1.0.0] - 2024-08-15

### Initial Release
- Basic repository analysis with topic filtering
- GPT-4 powered commit summarization
- Timeline visualization
- React frontend with FastAPI backend
- Support for auth, api, database, and ui topics