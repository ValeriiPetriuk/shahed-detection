<h1 align="center">🛡️ Shahed Detection</h1>

<p align="center">
  <img src="https://github.com/user-attachments/assets/70b248b0-a155-4b7d-9132-3594e5f8fed1" width="300" alt="Shahed Detection Screenshot"/>
</p>

<hr/>

<h2>🚀 How to Run the Project</h2>

<p>Follow these steps to set up and run the <strong>Shahed Detection System</strong> locally using Docker.</p>

<h3>🔧 Environment Setup</h3>

<ol>
  <li>Clone the repository:
    <pre><code>git clone https://github.com/ValeriiPetriuk/shahed-detection.git
cd shahed-detection</code></pre>
  </li>

  <li>Create a <code>.env</code> file in the root directory and add the following variables:
    <pre><code>BOT_TOKEN=BOT_TOKEN
ADMINS_ID=TG_ADMIN_ID</code></pre>
  </li>
</ol>

<h3>🐳 Run with Docker Compose</h3>

<pre><code>docker-compose up --build</code></pre>

<p>This will build and start the following services:</p>

<ul>
  <li><strong>Django</strong> – backend server with API</li>
  <li><strong>PostgreSQL</strong> – database</li>
  <li><strong>Redis</strong> – message broker for Celery</li>
  <li><strong>Celery</strong> – background task processor</li>
</ul>

<p>After running, the Django app will be available at: <a href="http://localhost:8000" target="_blank">http://localhost:8000</a></p>
