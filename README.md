# BibleBot

BibleBot is a Python script that fetches a random Bible verse from
[bible-api.com](https://bible-api.com) and posts it to X using the
Tweepy library.  
The original BibleBot would send a Bible verse to any user that sent
#bverse to it.  
Because of new X API pricing structure, I am not sure I could afford
to just serve up X Posts as requested.  
So we will now just post a daily random Bible verse.  

Follow @McGoobot on [X](https://x.com) and click on the notification
:bell: to get your daily Bible verse.

## License

This project is licensed under the MIT License - see below for details:  

MIT License  

Copyright (c) 2025 Jeffrey B. McGough

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Authors

- Jeffrey B. McGough - @jmcgough  
  *Initial work and project creator*

## Acknowledgments

- This project was developed with assistance from:
  - Grok, an AI created by xAI.
  - Gemini 2.0 Flash - For additional AI support.
  - [Aider](https://github.com/paul-gauthier/aider) - An AI-powered coding assistant.
  - [bible-api.com](https://bible-api.com) - For providing the free Bible verse API.

## How to Use

1. **Prerequisites**:
   - Python 3.x
   - Install dependencies: `pip install requests tweepy systemd-python`
   (Note: `systemd-python` is optional for `journald` logging; `syslog` will be used if
   unavailable.)
   - An X developer account with API credentials.

2. **Setup**:
   - Set the following environment variables with your X API credentials:

     ```text
     export X_API_KEY="your-api-key"
     export X_API_SECRET="your-api-secret"
     export X_ACCESS_TOKEN="your-access-token"
     export X_ACCESS_TOKEN_SECRET="your-access-token-secret"
     ```

   - Save the script as `biblebot.py` and make it executable: `chmod +x biblebot.py`.

3. **Run**:
   - Execute the script: `./biblebot.py`
   - It will fetch a random verse and post it to X, logging the result.

## How to Contribute

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. **Fork the repository** - Click the "Fork" button at the top right of the repository page.
2. **Clone your fork** - `git clone https://github.com/your-username/biblebot.git`
3. **Create a branch** - `git checkout -b your-feature-branch`
4. **Make your changes** - Add features, fix bugs, or improve documentation.
5. **Commit your changes** - `git commit -m "Describe your changes here"`
6. **Push to your fork** - `git push origin your-feature-branch`
7. **Submit a pull request** - Go to the original repository and create a pull request from your branch.

Please ensure your code follows Python PEP 8 style guidelines and includes appropriate comments.
Feel free to open an issue first if you want to discuss your ideas!
