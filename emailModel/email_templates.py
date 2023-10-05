
def get_verification_email_body_text(link):
    return f'''Thank you for registering with ExitMA. 
    We are thrilled to have you on board! 
    To get started and access ExitMA's full features, please verify your email by clicking the link below.
    {link}

    If the link doesn't work, copy and paste the following URL into your browser:
    {link}

    Get ready to discover the business that's perfect for you!

    Warm regards,
    The ExitMA Team'''

def get_verification_email_body_html(link, image_url=''):
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Verification</title>
        <style>
        .email-body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                font: 24px;
                text-align: left;
                }}
            .button {{
                background-color: #C40000;
                border: none;
                border-radius: 0.7rem;
                color: white;
                padding: 7px 16px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                transition: padding 0s, border 0s, color 0.5s, background-color 0.5s;
                }}
            .button:hover {{
                color: #C40000;
                background-color: white;
                padding: 6px 15px;
                border: 2px solid #C40000;
                }}
            .logo {{
                height: 6.5rem;
                width: 10rem;
            }}
        </style>
    </head>
    <body>
    <div class="email-body">
        <p>Thank you for registering with ExitMA. We are thrilled to have you on board!</p>
        <p>To get started and access ExitMA's full features, please verify your email by clicking the button below.</p>
        <a href="{link}" class="button">Verify Email</a>
    <br>
        <p>If the link doesn't work, copy and paste the following URL into your browser:</p>
        <p><a href="{link}">{link}</a></p>
    <br>
        <p>Get ready to discover the business that's perfect for you!</p>
    <br>
        <p>Warm regards,</p>
        <p>The ExitMA Team</p>
        <img class="logo" src="{image_url}" alt="ExitMA Logo">
    </div>
    </body>
    </html>
    '''

def get_newsletter_email_body_text():
    return f'''test text'''

def get_newsletter_email_body_html():
    return f'''test <p> html </p>'''