# Zoho CRM Cat Breeds Contact Creator

## Description
I created this script to automate the creation of contacts in Zoho CRM based on a list of cat breeds from the [catfact.ninja](https://catfact.ninja/) API. The script calls the `/breeds` endpoint to get a list of cat breeds. For each breed with an origin of "Natural", the script creates a contact in Zoho CRM with the following details:
- **First Name**: The breed name.
- **Last Name**: The breed name.
- **Email**: The breed name (with spaces replaced by underscores) followed by `@gmail.com`.

The script is designed to be idempotent, meaning if I run it multiple times, it does not create duplicate contacts in Zoho CRM. I avoided using an external database to ensure this idempotence.

## Prerequisites
To run this script, you'll need:
- Python 3.x and `pip` installed on your system.
- A Zoho CRM account (a free trial is fine).
- The Zoho CRM SDK for Python.

## Installation
Here are the steps to set up the environment and install the necessary dependencies:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
2. **Install the dependencies:**:
   ```bash
   pip install -r requirements.txt
3. **Set up your Zoho CRM account::**:
- Set up your Zoho CRM account:
- Create a Zoho CRM account.
- Configure your API keys and permissions as outlined in the Zoho CRM SDK guide.

## Usage
Here's how I use the script to create contacts in Zoho CRM from the catfact.ninja API:
- The script calls the /breeds endpoint on catfact.ninja to extract the cat breeds.
- For each breed with an origin of "Natural", the script creates a contact in Zoho CRM.
- The script ensures no duplicate contacts are created through idempotent techniques.
   ```bash
   python create_zoho_contacts.py
