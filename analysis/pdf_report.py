from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf_report(
        total_restaurants,
        avg_rating,
        total_votes,
        avg_cost
):

    pdf = SimpleDocTemplate(
        "static/reports/zomato_report.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Restaurant Analytics Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1,20)
    )

    content.append(
        Paragraph(
            f"Total Restaurants: {total_restaurants}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Average Rating: {avg_rating}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Total Votes: {total_votes}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Average Cost: {avg_cost}",
            styles["BodyText"]
        )
    )

    pdf.build(content)