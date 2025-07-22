from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")

class TravelRequest(BaseModel):
    from_location: str
    to_location: str
    departure_time: str
    return_time: Optional[str] = None
    budget: float
    disability_needs: Optional[bool] = False
    email: str
    phone: Optional[str] = ""
    purpose: Optional[str] = "personal"

class TicketOption(BaseModel):
    mode: str
    provider: str
    price: float
    duration: str
    transfer: Optional[List[str]] = []
    booking_link: str

class BookingConfirmation(BaseModel):
    ticket: TicketOption
    booking_id: str

class PaymentStatus(BaseModel):
    status: str
    amount: float
    reference: str

@app.post("/agent1/find_tickets")
def find_tickets(req: TravelRequest) -> List[TicketOption]:
    return [
        TicketOption(mode="flight", provider="Skyscanner", price=230.0, duration="3h 45m", transfer=["London", "Frankfurt"], booking_link="https://skyscanner.com/booking"),
        TicketOption(mode="train", provider="Eurostar", price=180.0, duration="5h 15m", transfer=["Brussels"], booking_link="https://eurostar.com/booking")
    ]

@app.post("/agent2/book_ticket")
def book_ticket(ticket: TicketOption) -> BookingConfirmation:
    return BookingConfirmation(ticket=ticket, booking_id="ABC123456")

@app.post("/agent3/route_plan")
def route_plan(booking: BookingConfirmation, req: TravelRequest):
    return {
        "steps": [
            "Taxi from home to airport/station",
            f"{booking.ticket.mode.title()} with {booking.ticket.provider}",
            "Taxi from arrival to hotel/destination"
        ],
        "accessible": req.disability_needs
    }

@app.post("/agent4/pay")
def pay_ticket(booking: BookingConfirmation) -> PaymentStatus:
    return PaymentStatus(status="paid", amount=booking.ticket.price, reference="PAY-987654321")

@app.post("/agent5/notify")
def send_notification(req: TravelRequest, booking: BookingConfirmation):
    msg = f"Trip from {req.from_location} to {req.to_location} booked via {booking.ticket.provider}. Booking ID: {booking.booking_id}."
    return {"status": "notified", "method": "email/sms (simulated)", "message": msg}

@app.post("/agent6/itinerary")
def generate_itinerary(req: TravelRequest):
    items = ["Passport", "Phone charger", "Travel adapter", "Comfortable shoes", "Toiletries", "Clothes for 3 days"]
    if req.purpose == "business":
        items.extend(["Laptop", "Business cards"])
    if req.disability_needs:
        items.append("Mobility aids (if applicable)")
    return {"packing_list": items, "purpose": req.purpose, "tips": "Check weather before packing."}

@app.post("/orchestrate")
def orchestrate(req: TravelRequest):
    tickets = find_tickets(req)
    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found.")
    booking = book_ticket(tickets[0])
    route = route_plan(booking, req)
    payment = pay_ticket(booking)
    notification = send_notification(req, booking)
    itinerary = generate_itinerary(req)
    return {"booking": booking, "route": route, "payment": payment, "notification": notification, "itinerary": itinerary}