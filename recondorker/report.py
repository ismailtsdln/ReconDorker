import json
import csv
from datetime import datetime
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReconDorker Report - {{ target }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); }
    </style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen pb-12">
    <div class="max-w-6xl mx-auto px-4 py-8">
        <header class="mb-12 flex justify-between items-center">
            <div>
                <h1 class="text-4xl font-bold text-slate-800 tracking-tight">ReconDorker <span class="text-blue-600">Report</span></h1>
                <p class="text-slate-500 mt-1 uppercase text-xs font-semibold tracking-widest">Target: {{ target }}</p>
            </div>
            <div class="text-right">
                <p class="text-sm text-slate-400">Generated on</p>
                <p class="text-slate-600 font-medium">{{ timestamp }}</p>
            </div>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div class="glass p-6 rounded-2xl shadow-sm border border-slate-200">
                <p class="text-slate-500 text-sm font-medium">Total Results</p>
                <p class="text-3xl font-bold text-blue-600">{{ results|length }}</p>
            </div>
            <div class="glass p-6 rounded-2xl shadow-sm border border-slate-200">
                <p class="text-slate-500 text-sm font-medium">Potential Leaks</p>
                <p class="text-3xl font-bold text-red-500">{{ results|selectattr('source', 'defined')|list|length }}</p>
            </div>
            <div class="glass p-6 rounded-2xl shadow-sm border border-slate-200">
                <p class="text-slate-500 text-sm font-medium">Status</p>
                <p class="text-3xl font-bold text-green-500">Completed</p>
            </div>
        </div>

        <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
            <table class="w-full text-left">
                <thead class="bg-slate-50 border-bottom border-slate-100">
                    <tr>
                        <th class="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Source</th>
                        <th class="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Result</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                    {% for result in results %}
                    <tr class="hover:bg-slate-50/50 transition-colors">
                        <td class="px-6 py-6 align-top">
                            <span class="px-2 py-1 rounded text-[10px] font-bold uppercase tracking-tighter 
                                {% if result.source == 'Google' %}bg-blue-100 text-blue-700
                                {% elif result.source == 'Bing' %}bg-green-100 text-green-700
                                {% else %}bg-orange-100 text-orange-700{% endif %}">
                                {{ result.source }}
                            </span>
                        </td>
                        <td class="px-6 py-6">
                            <a href="{{ result.link }}" target="_blank" class="text-lg font-bold text-slate-800 hover:text-blue-600 block mb-1">
                                {{ result.title }}
                            </a>
                            <p class="text-sm text-slate-500 leading-relaxed max-w-2xl">{{ result.snippet }}</p>
                            
                            {% if result.metadata %}
                            <div class="mt-3 p-3 bg-slate-50 rounded-xl border border-slate-100">
                                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Document Metadata</p>
                                <div class="grid grid-cols-2 gap-2">
                                    {% for key, value in result.metadata.items() %}
                                    <div class="text-[11px]">
                                        <span class="text-slate-400">{{ key }}:</span>
                                        <span class="text-slate-600 font-medium">{{ value }}</span>
                                    </div>
                                    {% endfor %}
                                </div>
                            </div>
                            {% endif %}

                            <p class="text-[10px] text-slate-400 font-mono mt-2 truncate">{{ result.link }}</p>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <footer class="mt-16 text-center text-slate-400 text-xs">
            <p>Generated by ReconDorker Pro — Automated OSINT Tool</p>
        </footer>
    </div>
</body>
</html>
"""

class Reporter:
    @staticmethod
    def to_json(results, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)

    @staticmethod
    def to_csv(results, output_file):
        if not results:
            return
        keys = results[0].keys()
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)

    @staticmethod
    def to_html(target, results, output_file):
        template = Template(HTML_TEMPLATE)
        html_content = template.render(
            target=target,
            results=results,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
