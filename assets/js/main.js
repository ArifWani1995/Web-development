const themeToggle = document.querySelector(".theme-toggle");
const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");
const skillsGrid = document.getElementById("skills-grid");
const projectsGrid = document.getElementById("projects-grid");
const filterButtons = document.getElementById("filter-buttons");
const projectSearch = document.getElementById("project-search");
const testimonialsGrid = document.getElementById("testimonials-grid");
const contactForm = document.getElementById("contact-form");
const formStatus = document.getElementById("form-status");

const fallbackData = {
  skills: [
    {
      category: "Programming Languages",
      items: [
        { name: "JavaScript", level: 90, icon: "fa-brands fa-js" },
        { name: "Python", level: 85, icon: "fa-brands fa-python" },
        { name: "Java", level: 75, icon: "fa-brands fa-java" },
        { name: "SQL", level: 78, icon: "fa-solid fa-database" }
      ]
    },
    {
      category: "Web Technologies",
      items: [
        { name: "HTML5", level: 95, icon: "fa-brands fa-html5" },
        { name: "CSS3", level: 92, icon: "fa-brands fa-css3-alt" },
        { name: "REST APIs", level: 82, icon: "fa-solid fa-code" },
        { name: "Accessibility", level: 70, icon: "fa-solid fa-universal-access" }
      ]
    },
    {
      category: "Tools & Frameworks",
      items: [
        { name: "React", level: 80, icon: "fa-brands fa-react" },
        { name: "Node.js", level: 78, icon: "fa-brands fa-node" },
        { name: "Git & GitHub", level: 88, icon: "fa-brands fa-github" },
        { name: "Figma", level: 72, icon: "fa-brands fa-figma" }
      ]
    }
  ],
  projects: [
    {
      title: "Portfolio Launchpad",
      description: "A responsive portfolio template with dynamic sections, reusable components, and accessible design patterns.",
      technologies: ["HTML5", "CSS3", "JavaScript"],
      category: "Web",
      image: "assets/images/project-1.svg",
      demo: "https://example.com",
      source: "https://github.com/yourname/portfolio-launchpad"
    },
    {
      title: "Insights Dashboard",
      description: "Interactive analytics dashboard with filterable metrics, charts, and export-ready reports.",
      technologies: ["React", "Node.js", "Chart.js"],
      category: "Data Science",
      image: "assets/images/project-2.svg",
      demo: "https://example.com",
      source: "https://github.com/yourname/insights-dashboard"
    },
    {
      title: "Smart Campus Assistant",
      description: "Campus helper app that delivers smart notifications, event tracking, and AI-assisted study tips.",
      technologies: ["Python", "Flask", "SQLite"],
      category: "ML",
      image: "assets/images/project-3.svg",
      demo: "https://example.com",
      source: "https://github.com/yourname/smart-campus-assistant"
    }
  ],
  testimonials: [
    {
      name: "Alex Morgan",
      role: "Tech Mentor",
      quote: "A creative builder who blends clean UI with thoughtful engineering. Always delivers on time."
    },
    {
      name: "Jamie Patel",
      role: "Hackathon Judge",
      quote: "Impressed by the clarity of the presentation and the ability to communicate technical ideas."
    }
  ]
};

let allProjects = [];
let activeFilter = "All";

const setTheme = (mode) => {
  document.documentElement.setAttribute("data-theme", mode);
  localStorage.setItem("theme", mode);
  themeToggle.innerHTML = mode === "dark" ? "<i class=\"fa-solid fa-sun\"></i>" : "<i class=\"fa-solid fa-moon\"></i>";
};

const initializeTheme = () => {
  const storedTheme = localStorage.getItem("theme");
  if (storedTheme) {
    setTheme(storedTheme);
  }
};

themeToggle.addEventListener("click", () => {
  const currentTheme = document.documentElement.getAttribute("data-theme") || "light";
  setTheme(currentTheme === "light" ? "dark" : "light");
});

navToggle.addEventListener("click", () => {
  navLinks.classList.toggle("open");
});

const createSkillCard = (category) => {
  const card = document.createElement("div");
  card.className = "skill-card";
  card.innerHTML = `<h3>${category.category}</h3>`;

  category.items.forEach((skill) => {
    const item = document.createElement("div");
    item.className = "skill-item";
    item.innerHTML = `
      <header>
        <div class="label">
          <i class="${skill.icon}"></i>
          <span>${skill.name}</span>
        </div>
        <strong>${skill.level}%</strong>
      </header>
      <div class="skill-bar"><span data-level="${skill.level}"></span></div>
    `;
    card.appendChild(item);
  });

  return card;
};

const renderSkills = (skills) => {
  skillsGrid.innerHTML = "";
  skills.forEach((category) => {
    skillsGrid.appendChild(createSkillCard(category));
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.width = `${entry.target.dataset.level}%`;
        }
      });
    },
    { threshold: 0.5 }
  );

  document.querySelectorAll(".skill-bar span").forEach((bar) => observer.observe(bar));
};

const buildFilters = (projects) => {
  const categories = ["All", ...new Set(projects.map((project) => project.category))];
  filterButtons.innerHTML = "";

  categories.forEach((category) => {
    const button = document.createElement("button");
    button.textContent = category;
    button.className = category === "All" ? "active" : "";
    button.addEventListener("click", () => {
      activeFilter = category;
      document.querySelectorAll(".filter-buttons button").forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");
      renderProjects();
    });
    filterButtons.appendChild(button);
  });
};

const createProjectCard = (project) => {
  const card = document.createElement("article");
  card.className = "project-card";
  card.innerHTML = `
    <img src="${project.image}" alt="${project.title} preview" loading="lazy" />
    <div class="project-content">
      <h3>${project.title}</h3>
      <p>${project.description}</p>
      <div class="tech-tags">
        ${project.technologies.map((tech) => `<span>${tech}</span>`).join("")}
      </div>
      <div class="project-links">
        <a href="${project.demo}" target="_blank" rel="noreferrer">Live Demo</a>
        <a href="${project.source}" target="_blank" rel="noreferrer">Source Code</a>
      </div>
    </div>
  `;
  return card;
};

const renderProjects = () => {
  const query = projectSearch.value.toLowerCase();
  const filtered = allProjects.filter((project) => {
    const matchesCategory = activeFilter === "All" || project.category === activeFilter;
    const matchesSearch = project.title.toLowerCase().includes(query) || project.description.toLowerCase().includes(query);
    return matchesCategory && matchesSearch;
  });

  projectsGrid.innerHTML = "";
  filtered.forEach((project) => projectsGrid.appendChild(createProjectCard(project)));
};

projectSearch.addEventListener("input", renderProjects);

const renderTestimonials = (testimonials) => {
  testimonialsGrid.innerHTML = "";
  testimonials.forEach((testimonial) => {
    const card = document.createElement("div");
    card.className = "testimonial-card";
    card.innerHTML = `
      <p>“${testimonial.quote}”</p>
      <h4>${testimonial.name}</h4>
      <span>${testimonial.role}</span>
    `;
    testimonialsGrid.appendChild(card);
  });
};

contactForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const name = contactForm.name.value.trim();
  const email = contactForm.email.value.trim();
  const message = contactForm.message.value.trim();

  if (!name || !email || !message) {
    formStatus.textContent = "Please complete all fields before sending.";
    return;
  }

  if (!/\S+@\S+\.\S+/.test(email)) {
    formStatus.textContent = "Please enter a valid email address.";
    return;
  }

  formStatus.textContent = "Thanks! Your message has been sent.";
  contactForm.reset();
});

const dataUrl = new URL("./assets/data/data.json", window.location.href);

fetch(dataUrl)
  .then((response) => response.json())
  .then((data) => {
    renderSkills(data.skills);
    allProjects = data.projects;
    buildFilters(allProjects);
    renderProjects();
    renderTestimonials(data.testimonials);
  })
  .catch(() => {
    renderSkills(fallbackData.skills);
    allProjects = fallbackData.projects;
    buildFilters(allProjects);
    renderProjects();
    renderTestimonials(fallbackData.testimonials);
    skillsGrid.insertAdjacentHTML(
      "afterbegin",
      "<p>Using offline data. Update assets/data/data.json when available.</p>"
    );
  });

initializeTheme();
