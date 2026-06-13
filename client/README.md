# Weather Travel Assistant - Frontend

A modern, responsive React + Vite + TypeScript weather application that provides real-time weather data and travel planning features.

## Features

✅ **Weather Search**
- Search by city name
- Search by ZIP/postal code
- Search by geographic coordinates (lat, lon)
- Search by landmarks

✅ **Current Location Detection**
- Browser geolocation support
- One-click access to current weather

✅ **Weather Display**
- Real-time temperature and conditions
- "Feels like" temperature
- Humidity, wind speed, pressure, visibility
- Beautiful weather icons

✅ **5-Day Forecast**
- Daily temperature ranges
- Weather conditions
- Precipitation probability
- Interactive forecast cards

✅ **Save & Manage Locations**
- Save favorite locations
- Quick access to saved weather
- Delete saved locations
- View location history

✅ **Location Mapping**
- Embedded Google Maps
- Quick location visualization

✅ **Data Export**
- Export saved locations as JSON
- Export saved locations as CSV

✅ **Responsive Design**
- Works on desktop, tablet, and mobile
- Mobile-first approach
- Touch-friendly interface

✅ **Error Handling**
- User-friendly error messages
- Graceful degradation
- Network error handling
- Input validation

## Tech Stack

- **React 18** - UI library
- **Vite 5** - Build tool
- **TypeScript** - Type safety
- **Axios** - HTTP client
- **React Icons** - Icon library
- **CSS Modules** - Scoped styling

## Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

## Building

```bash
npm run build
```

This creates an optimized production build in the `dist/` folder.

## Project Structure

```
src/
├── components/           # React components
│   ├── SearchBar.tsx
│   ├── CurrentWeather.tsx
│   ├── Forecast.tsx
│   ├── SavedLocations.tsx
│   ├── MapView.tsx
│   └── ErrorMessage.tsx
├── services/            # API service layer
│   └── api.ts
├── utils/               # Utility functions
│   └── weather.ts
├── App.tsx              # Main app component
├── App.module.css
├── main.tsx
└── index.css

```

## API Integration

The frontend communicates with the backend via REST API:

```
Base URL: http://localhost:8000/api

Endpoints:
- GET /weather/current - Current weather
- GET /weather/forecast - 5-day forecast
- GET /geocode - Convert location to coordinates
- GET /reverse-geocode - Convert coordinates to location
- GET /locations - Get saved locations
- POST /locations - Create new saved location
- PUT /locations/{id} - Update saved location
- DELETE /locations/{id} - Delete saved location
- GET /export - Export data (JSON/CSV)
```

## Responsive Design Features

- **Desktop (1200px+)**: Full layout with sidebar
- **Tablet (768-1199px)**: Adjusted spacing and grid layout
- **Mobile (< 768px)**: Optimized single-column layout

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Environment Variables

Optional: Create a `.env` file for API configuration:

```env
VITE_API_URL=http://localhost:8000/api
```

## Development Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check

# Linting
npm run lint
```

## Key Components

### SearchBar
- Input field for location search
- Current location button (geolocation)
- Loading state management

### CurrentWeather
- Main weather display
- Temperature, conditions, "feels like"
- Additional metrics (humidity, wind, pressure, visibility)
- Save location button

### Forecast
- 5-day weather forecast
- Daily temp ranges
- Weather conditions
- Precipitation probability

### SavedLocations
- List of saved weather searches
- Quick location switching
- Delete functionality
- Export buttons (JSON/CSV)

### MapView
- Google Maps embed
- Location visualization

### ErrorMessage
- User-friendly error display
- Dismissible alerts
- Color-coded messages

## Weather Icons

Uses `react-icons` (Weather Icons) for weather condition visualization:
- Clear/Cloudy
- Rain/Snow
- Thunderstorms
- Fog/Haze
- And more...

## Styling

- **CSS Modules** for component scoping
- **Gradient background** for visual appeal
- **Glassmorphism** effects for cards
- **Mobile-first** responsive design
- **Animations** for smooth interactions

## Error Handling Examples

1. **Location Not Found**
   - Displays user-friendly error message
   - Suggests trying another search

2. **Geolocation Denied**
   - Graceful handling of permission denial
   - Allows manual location search

3. **API Failures**
   - Network error handling
   - Retry-friendly interface
   - Clear error messages

## Performance Optimizations

- Code splitting with Vite
- CSS Module optimization
- Efficient re-renders with React hooks
- Image and icon optimization
- Lazy loading of components

## Accessibility

- Semantic HTML structure
- ARIA labels for buttons
- Keyboard navigation support
- Color contrast compliance
- Mobile-friendly touch targets

## Future Enhancements

- Dark mode toggle
- Temperature unit conversion (°C/°F)
- Weather alerts
- Historical weather data
- Advanced analytics
- Push notifications
- PWA capabilities

## Support & Feedback

For issues or suggestions, please create an issue in the GitHub repository.

---

Built with ❤️ for PM Accelerator AI Engineer Assessment
