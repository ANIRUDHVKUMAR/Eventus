
### Eventus ###

Eventus Dashboard is a web application designed for managing and viewing events across multiple clubs. The application features functionality for club administrators to add, modify, and remove events, as well as for users to register and unregister from events.

## Features

- **Club Admin Dashboard**:
  - **Add Event**: Allows club admins to create new events with details like date, time, title, venue, and description.
  - **Modify Event**: Enables club admins to update event details.
  - **Remove Event**: Provides functionality to delete events.
  - **Past Events**: Displays a list of past events with participant details.

- **User Dashboard**:
  - **Event Registration**: Users can register for events organized by various clubs.
  - **Event Unregistration**: Users can unregister from events they have previously registered for.
  - **Club Filter**: Allows users to filter events by club.

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/eventus-dashboard.git
   cd eventus-dashboard
   ```

2. **Setup Backend**:
   - **Create and Activate Virtual Environment**:
     ```bash
     python -m venv venv
     source venv/bin/activate   # On Windows use `venv\Scripts\activate`
     ```
   - **Install Dependencies**:
     ```bash
     pip install -r requirements.txt
     ```
  
3. **Run the Application**:
   - **Start Flask Backend**:
     ```bash
     python app.py
     ```
   - **Run Frontend Build** (if applicable):
     ```bash
     npm run build
     ```

## Usage

1. **Access the Application**:
   - Open your web browser and go to `http://localhost:5000` to access the Eventus Dashboard.

2. **Login as Club Admin**:
   - Enter valid credentials to access the Club Admin Dashboard.

3. **Manage Events**:
   - Use the Club Admin Dashboard to add, modify, or remove events.
   - View past events with participant details.

4. **User Interaction**:
   - Register and unregister for events on the User Dashboard.
   - Filter events by club.

## Endpoints

### Club Admin Endpoints

- `POST /add_event`: Add a new event.
- `POST /modify_event`: Modify an existing event.
- `POST /remove_event`: Remove an existing event.
- `GET /past_events`: Retrieve past events with participant details.

### User Endpoints

- `POST /register_event/<event_id>`: Register for an event.
- `POST /unregister_event/<event_id>`: Unregister from an event.

## Contributing

1. **Fork the Repository**: Click on the "Fork" button on GitHub.
2. **Create a Branch**: Create a new branch for your changes.
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Changes**: Implement your changes and commit them.
   ```bash
   git add .
   git commit -m "Add your commit message"
   ```
4. **Push Changes**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a Pull Request**: Open a pull request on GitHub with a description of your changes.


## Contact

For any inquiries or issues, please contact [anirudhvk2002@gmail.com](mailto:anirudhvk2002@gmail.com).
