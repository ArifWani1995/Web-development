const unemploymentTrend = [
  { year: 2015, rate: 6.9 },
  { year: 2016, rate: 7.4 },
  { year: 2017, rate: 8.1 },
  { year: 2018, rate: 8.8 },
  { year: 2019, rate: 9.7 },
  { year: 2020, rate: 11.5 },
  { year: 2021, rate: 10.8 },
  { year: 2022, rate: 9.9 },
  { year: 2023, rate: 9.2 },
  { year: 2024, rate: 8.7 },
  { year: 2025, rate: 8.1 }
];

const districtData = [
  { district: "Srinagar", unemployment: 11.4, year: 2025, sector: "Services" },
  { district: "Jammu", unemployment: 9.8, year: 2025, sector: "Services" },
  { district: "Anantnag", unemployment: 8.6, year: 2025, sector: "Agriculture" },
  { district: "Baramulla", unemployment: 9.1, year: 2025, sector: "Agriculture" },
  { district: "Pulwama", unemployment: 8.3, year: 2025, sector: "Industry" },
  { district: "Kupwara", unemployment: 8.8, year: 2025, sector: "Agriculture" },
  { district: "Kathua", unemployment: 7.6, year: 2025, sector: "Industry" },
  { district: "Budgam", unemployment: 9.4, year: 2025, sector: "Services" },
  { district: "Srinagar", unemployment: 12.1, year: 2024, sector: "Services" },
  { district: "Jammu", unemployment: 10.2, year: 2024, sector: "Services" },
  { district: "Anantnag", unemployment: 9.1, year: 2024, sector: "Agriculture" },
  { district: "Baramulla", unemployment: 9.8, year: 2024, sector: "Agriculture" },
  { district: "Pulwama", unemployment: 8.7, year: 2024, sector: "Industry" },
  { district: "Kupwara", unemployment: 9.2, year: 2024, sector: "Agriculture" },
  { district: "Kathua", unemployment: 8.2, year: 2024, sector: "Industry" },
  { district: "Budgam", unemployment: 9.9, year: 2024, sector: "Services" }
];

const sectorShare = {
  Agriculture: 43,
  Industry: 22,
  Services: 35
};

let sortState = { key: "year", asc: false };
let selectedGender = "Male";
let selectedRegion = "Urban";
let tableData = [...districtData];

const yearFilter = document.getElementById("yearFilter");
const districtFilter = document.getElementById("districtFilter");
const tableBody = document.getElementById("tableBody");
const tableSearch = document.getElementById("tableSearch");
const genderToggle = document.getElementById("genderToggle");
const regionToggle = document.getElementById("regionToggle");
const darkModeToggle = document.getElementById("darkModeToggle");

let lineChart;
let barChart;
let pieChart;

function initializeFilters() {
  const years = [...new Set(districtData.map((d) => d.year))].sort((a, b) => b - a);
  yearFilter.innerHTML = `<option value="all">All Years</option>${years.map((y) => `<option value="${y}">${y}</option>`).join("")}`;

  const districts = [...new Set(districtData.map((d) => d.district))].sort();
  districtFilter.innerHTML = `<option value="all">All Districts</option>${districts.map((d) => `<option value="${d}">${d}</option>`).join("")}`;
}

function renderKPI(filtered) {
  const avgUnemployment = filtered.reduce((sum, item) => sum + item.unemployment, 0) / (filtered.length || 1);
  const youth = avgUnemployment + (selectedGender === "Female" ? 3.2 : 2.4);
  const urban = avgUnemployment + (selectedRegion === "Urban" ? 1.1 : -0.9);
  const rural = avgUnemployment + (selectedRegion === "Urban" ? -0.8 : 0.8);
  const latest = unemploymentTrend[unemploymentTrend.length - 1].rate;
  const previous = unemploymentTrend[unemploymentTrend.length - 2].rate;
  const growth = (((latest - previous) / previous) * 100).toFixed(1);

  animateCounter("kpi-total", avgUnemployment, "%");
  animateCounter("kpi-youth", youth, "%");
  document.getElementById("kpi-urban-rural").textContent = `${urban.toFixed(1)}% / ${rural.toFixed(1)}%`;
  document.getElementById("kpi-growth").textContent = `${growth}%`;
}

function animateCounter(id, value, suffix = "") {
  const counter = new countUp.CountUp(id, value, {
    decimalPlaces: 1,
    duration: 1.5,
    suffix
  });
  if (!counter.error) counter.start();
}

function initCharts() {
  lineChart = new Chart(document.getElementById("lineChart"), {
    type: "line",
    data: {
      labels: unemploymentTrend.map((d) => d.year),
      datasets: [{
        label: "Unemployment %",
        data: unemploymentTrend.map((d) => d.rate),
        borderColor: "#7c3aed",
        backgroundColor: "rgba(124,58,237,0.15)",
        fill: true,
        tension: 0.35,
        pointRadius: 4
      }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  barChart = new Chart(document.getElementById("barChart"), {
    type: "bar",
    data: {
      labels: [],
      datasets: [{
        label: "Unemployment %",
        data: [],
        backgroundColor: ["#3b82f6", "#8b5cf6", "#06b6d4", "#f97316", "#14b8a6", "#ef4444", "#84cc16", "#ec4899"]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { y: { beginAtZero: true } }
    }
  });

  pieChart = new Chart(document.getElementById("pieChart"), {
    type: "pie",
    data: {
      labels: Object.keys(sectorShare),
      datasets: [{
        data: Object.values(sectorShare),
        backgroundColor: ["#22c55e", "#f97316", "#0ea5e9"]
      }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });
}

function applyFilters() {
  const year = yearFilter.value;
  const district = districtFilter.value;

  tableData = districtData.filter((row) => {
    const byYear = year === "all" || String(row.year) === year;
    const byDistrict = district === "all" || row.district === district;
    return byYear && byDistrict;
  });

  updateBarChart(tableData);
  renderKPI(tableData);
  renderTable();
}

function updateBarChart(data) {
  barChart.data.labels = data.map((d) => d.district);
  barChart.data.datasets[0].data = data.map((d) => d.unemployment);
  barChart.update();
}

function renderTable() {
  const query = tableSearch.value.toLowerCase().trim();
  const filtered = tableData.filter((row) =>
    [row.year, row.district, row.unemployment, row.sector].join(" ").toLowerCase().includes(query)
  );

  const sorted = [...filtered].sort((a, b) => {
    const { key, asc } = sortState;
    const left = a[key];
    const right = b[key];
    if (typeof left === "number") return asc ? left - right : right - left;
    return asc ? String(left).localeCompare(String(right)) : String(right).localeCompare(String(left));
  });

  tableBody.innerHTML = sorted
    .map(
      (row) => `
      <tr>
        <td>${row.year}</td>
        <td>${row.district}</td>
        <td>${row.unemployment.toFixed(1)}%</td>
        <td>${row.sector}</td>
      </tr>`
    )
    .join("");
}

function bindEvents() {
  [yearFilter, districtFilter].forEach((el) => el.addEventListener("change", applyFilters));
  tableSearch.addEventListener("input", renderTable);

  document.querySelectorAll("th[data-sort]").forEach((header) => {
    header.addEventListener("click", () => {
      const key = header.dataset.sort;
      if (sortState.key === key) sortState.asc = !sortState.asc;
      else sortState = { key, asc: true };
      renderTable();
    });
  });

  genderToggle.addEventListener("click", () => {
    selectedGender = selectedGender === "Male" ? "Female" : "Male";
    genderToggle.textContent = selectedGender;
    applyFilters();
  });

  regionToggle.addEventListener("click", () => {
    selectedRegion = selectedRegion === "Urban" ? "Rural" : "Urban";
    regionToggle.textContent = selectedRegion;
    applyFilters();
  });

  darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
  });
}

function initAnimations() {
  AOS.init({ duration: 800, once: true });
  gsap.from(".kpi-card", {
    y: 40,
    opacity: 0,
    duration: 0.9,
    stagger: 0.12,
    ease: "power3.out"
  });
}

window.addEventListener("load", () => {
  document.body.classList.add("loaded");
});

initializeFilters();
initCharts();
bindEvents();
applyFilters();
initAnimations();
