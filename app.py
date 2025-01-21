from flask import Flask, render_template, request

app = Flask(__name__)

# Fungsi untuk menghitung hasil

def calculate_queue_metrics(interarrival_time, service_time):
    # Laju kedatangan (lambda)
    arrival_rate = 1 / interarrival_time
    # Laju pelayanan per pelayan (mu)
    service_rate = 1 / service_time
    # Pemanfaatan pelayan (rho)
    utilization = arrival_rate / (2 * service_rate)
    # Waktu rata-rata dalam sistem (W)
    average_time_in_system = 1 / (service_rate - (arrival_rate / 2))
    # Waktu rata-rata dalam antrian (Wq)
    average_time_in_queue = (arrival_rate ** 2) / (2 * service_rate * (service_rate - (arrival_rate / 2)))

    steps = [
        f"Laju kedatangan (λ) = 1 / Waktu antar kedatangan = 1 / {interarrival_time} = {arrival_rate}",
        f"Laju pelayanan per pelayan (μ) = 1 / Waktu pelayanan = 1 / {service_time} = {service_rate}",
        f"Pemanfaatan pelayan (ρ) = λ / (2 * μ) = {arrival_rate} / (2 * {service_rate}) = {utilization}",
        f"Waktu rata-rata dalam sistem (W) = 1 / (μ - λ/2) = 1 / ({service_rate} - {arrival_rate}/2) = {average_time_in_system}",
        f"Waktu rata-rata dalam antrian (Wq) = λ^2 / (2 * μ * (μ - λ/2)) = {arrival_rate}^2 / (2 * {service_rate} * ({service_rate} - {arrival_rate}/2)) = {average_time_in_queue}"
    ]

    return {
        'arrival_rate': arrival_rate,
        'service_rate': service_rate,
        'utilization': utilization,
        'average_time_in_system': average_time_in_system,
        'average_time_in_queue': average_time_in_queue,
        'steps': steps
    }

# Halaman Input
@app.route('/')
def input_page():
    return render_template('input.html', title="Queuing Model Kalkulator M/M/2", subtitle="by Vivi Widia", tab_color="purple")

# Halaman Hasil
@app.route('/result', methods=['POST'])
def result_page():
    try:
        interarrival_time = float(request.form['interarrival_time'])
        service_time = float(request.form['service_time'])
        results = calculate_queue_metrics(interarrival_time, service_time)
        return render_template('result.html', results=results, title="Queuing Model Kalkulator M/M/2", subtitle="by Vivi Widia", tab_color="purple")
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
