import csv
import io
import json
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def _safe_json_loads(value, default):
    if not value:
        return default

    if isinstance(value, (dict, list)):
        return value

    try:
        return json.loads(value)
    except Exception:
        return default


def _weather_request_to_dict(request):
    return {
        "id": request.id,
        "location_query": request.location_query,
        "resolved_location": request.resolved_location,
        "latitude": request.latitude,
        "longitude": request.longitude,
        "start_date": str(request.start_date),
        "end_date": str(request.end_date),
        "current_weather": _safe_json_loads(request.current_weather, {}),
        "forecast_data": _safe_json_loads(request.forecast_data, []),
        "hourly_forecast": _safe_json_loads(request.hourly_forecast, []),
        "travel_tips": _safe_json_loads(request.travel_tips, []),
        "created_at": str(request.created_at),
        "updated_at": str(request.updated_at),
    }


def export_weather_requests_json(requests):
    data = [_weather_request_to_dict(request) for request in requests]
    return json.dumps(data, indent=2, default=str).encode("utf-8")


def export_weather_requests_csv(requests):
    output = io.StringIO()

    writer = csv.writer(output)
    writer.writerow([
        "ID",
        "Location Query",
        "Resolved Location",
        "Latitude",
        "Longitude",
        "Start Date",
        "End Date",
        "Temperature",
        "Description",
        "Humidity",
        "Wind Speed",
        "Travel Tips",
        "Created At",
    ])

    for request in requests:
        current_weather = _safe_json_loads(request.current_weather, {})
        travel_tips = _safe_json_loads(request.travel_tips, [])

        writer.writerow([
            request.id,
            request.location_query,
            request.resolved_location,
            request.latitude,
            request.longitude,
            request.start_date,
            request.end_date,
            current_weather.get("temperature", ""),
            current_weather.get("description", ""),
            current_weather.get("humidity", ""),
            current_weather.get("wind_speed", ""),
            " | ".join(travel_tips),
            request.created_at,
        ])

    return output.getvalue().encode("utf-8")


def export_weather_requests_pdf(requests):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    title = Paragraph("Weather Travel Assistant - Export Report", styles["Title"])
    story.append(title)
    story.append(Spacer(1, 12))

    generated = Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}",
        styles["Normal"],
    )
    story.append(generated)
    story.append(Spacer(1, 20))

    if not requests:
        story.append(Paragraph("No saved weather requests found.", styles["Normal"]))
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    for request in requests:
        current_weather = _safe_json_loads(request.current_weather, {})
        forecast_data = _safe_json_loads(request.forecast_data, [])
        travel_tips = _safe_json_loads(request.travel_tips, [])

        story.append(
            Paragraph(
                f"<b>{request.resolved_location}</b>",
                styles["Heading2"],
            )
        )

        summary_data = [
            ["Location Query", request.location_query],
            ["Date Range", f"{request.start_date} to {request.end_date}"],
            ["Coordinates", f"{request.latitude}, {request.longitude}"],
            ["Temperature", f"{current_weather.get('temperature', 'N/A')}°C"],
            ["Condition", current_weather.get("description", "N/A")],
            ["Humidity", f"{current_weather.get('humidity', 'N/A')}%"],
            ["Wind Speed", f"{current_weather.get('wind_speed', 'N/A')} km/h"],
            ["Saved At", str(request.created_at)],
        ]

        summary_table = Table(summary_data, colWidths=[120, 350])
        summary_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(summary_table)
        story.append(Spacer(1, 12))

        if travel_tips:
            story.append(Paragraph("<b>Weather Advisory / Travel Tips</b>", styles["Heading3"]))

            for tip in travel_tips:
                story.append(Paragraph(f"• {tip}", styles["Normal"]))

            story.append(Spacer(1, 12))

        if forecast_data:
            story.append(Paragraph("<b>5-Day Forecast</b>", styles["Heading3"]))

            forecast_table_data = [
                ["Date", "Condition", "High", "Low", "Rain Chance"]
            ]

            for day in forecast_data[:5]:
                forecast_table_data.append([
                    day.get("date", "N/A"),
                    day.get("description", "N/A"),
                    f"{day.get('temperature_max', 'N/A')}°C",
                    f"{day.get('temperature_min', 'N/A')}°C",
                    f"{day.get('precipitation_probability', 'N/A')}%",
                ])

            forecast_table = Table(
                forecast_table_data,
                colWidths=[90, 140, 70, 70, 90],
            )

            forecast_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("PADDING", (0, 0), (-1, -1), 6),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ])
            )

            story.append(forecast_table)
            story.append(Spacer(1, 20))

        story.append(Spacer(1, 16))

    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()