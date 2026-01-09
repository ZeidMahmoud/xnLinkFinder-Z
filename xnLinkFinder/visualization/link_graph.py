"""
Link Relationship Graph Generator
Build and visualize endpoint relationships
"""

import json
from typing import List, Dict, Set, Tuple
from pathlib import Path
from urllib.parse import urlparse


class LinkGraphGenerator:
    """Generate relationship graphs for discovered endpoints"""
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.clusters = {}
    
    def add_endpoint(self, url: str, metadata: Dict = None):
        """Add an endpoint to the graph"""
        parsed = urlparse(url)
        node_id = url
        
        self.nodes[node_id] = {
            'url': url,
            'path': parsed.path,
            'domain': parsed.netloc,
            'metadata': metadata or {},
            'type': self._classify_endpoint(url)
        }
    
    def add_relationship(self, source: str, target: str, rel_type: str = "links_to"):
        """Add a relationship between two endpoints"""
        self.edges.append({
            'source': source,
            'target': target,
            'type': rel_type
        })
    
    def _classify_endpoint(self, url: str) -> str:
        """Classify endpoint type"""
        url_lower = url.lower()
        
        if '/admin' in url_lower or '/dashboard' in url_lower:
            return 'admin'
        elif '/api/' in url_lower or '/v1/' in url_lower or '/v2/' in url_lower:
            return 'api'
        elif '/auth' in url_lower or '/login' in url_lower or '/oauth' in url_lower:
            return 'auth'
        elif '/user' in url_lower or '/account' in url_lower or '/profile' in url_lower:
            return 'user'
        elif '/upload' in url_lower or '/download' in url_lower or '/file' in url_lower:
            return 'file'
        else:
            return 'general'
    
    def cluster_by_functionality(self) -> Dict[str, List[str]]:
        """Cluster endpoints by functionality"""
        clusters = {}
        for node_id, node_data in self.nodes.items():
            node_type = node_data['type']
            if node_type not in clusters:
                clusters[node_type] = []
            clusters[node_type].append(node_id)
        
        self.clusters = clusters
        return clusters
    
    def calculate_centrality(self) -> Dict[str, float]:
        """Calculate centrality metrics (simplified)"""
        # Count incoming edges
        centrality = {node_id: 0 for node_id in self.nodes}
        for edge in self.edges:
            target = edge['target']
            if target in centrality:
                centrality[target] += 1
        
        # Normalize
        max_score = max(centrality.values()) if centrality.values() else 1
        if max_score > 0:
            centrality = {k: v / max_score for k, v in centrality.items()}
        
        return centrality
    
    def to_json(self) -> str:
        """Export graph as JSON"""
        graph_data = {
            'nodes': [
                {'id': node_id, **node_data}
                for node_id, node_data in self.nodes.items()
            ],
            'edges': self.edges,
            'clusters': self.clusters
        }
        return json.dumps(graph_data, indent=2)
    
    def to_dot(self) -> str:
        """Export graph as DOT format"""
        dot = "digraph EndpointGraph {\n"
        dot += "  rankdir=LR;\n"
        dot += "  node [shape=box];\n\n"
        
        # Add nodes with colors based on type
        colors = {
            'admin': 'red',
            'api': 'blue',
            'auth': 'orange',
            'user': 'green',
            'file': 'purple',
            'general': 'gray'
        }
        
        for node_id, node_data in self.nodes.items():
            color = colors.get(node_data['type'], 'gray')
            label = node_data['path'] or '/'
            dot += f'  "{node_id}" [label="{label}", color={color}];\n'
        
        dot += "\n"
        
        # Add edges
        for edge in self.edges:
            dot += f'  "{edge["source"]}" -> "{edge["target"]}";\n'
        
        dot += "}\n"
        return dot
    
    def to_gexf(self) -> str:
        """Export graph as GEXF format"""
        gexf = '<?xml version="1.0" encoding="UTF-8"?>\n'
        gexf += '<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">\n'
        gexf += '  <graph mode="static" defaultedgetype="directed">\n'
        
        # Nodes
        gexf += '    <nodes>\n'
        for i, (node_id, node_data) in enumerate(self.nodes.items()):
            gexf += f'      <node id="{i}" label="{node_data["path"]}">\n'
            gexf += f'        <attvalues>\n'
            gexf += f'          <attvalue for="0" value="{node_data["type"]}"/>\n'
            gexf += f'        </attvalues>\n'
            gexf += f'      </node>\n'
        gexf += '    </nodes>\n'
        
        # Edges
        gexf += '    <edges>\n'
        node_ids = list(self.nodes.keys())
        for i, edge in enumerate(self.edges):
            source_idx = node_ids.index(edge['source']) if edge['source'] in node_ids else 0
            target_idx = node_ids.index(edge['target']) if edge['target'] in node_ids else 0
            gexf += f'      <edge id="{i}" source="{source_idx}" target="{target_idx}"/>\n'
        gexf += '    </edges>\n'
        
        gexf += '  </graph>\n'
        gexf += '</gexf>\n'
        return gexf
    
    def to_html(self) -> str:
        """Generate interactive HTML visualization"""
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>xnLinkFinder - Endpoint Graph</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        #graph { width: 100%; height: 800px; border: 1px solid #ddd; }
        #legend { margin-top: 20px; }
        .legend-item { display: inline-block; margin-right: 20px; }
        .legend-color { display: inline-block; width: 20px; height: 20px; margin-right: 5px; vertical-align: middle; }
    </style>
</head>
<body>
    <h1>Endpoint Relationship Graph</h1>
    <div id="graph"></div>
    <div id="legend">
        <div class="legend-item"><span class="legend-color" style="background: red;"></span>Admin</div>
        <div class="legend-item"><span class="legend-color" style="background: blue;"></span>API</div>
        <div class="legend-item"><span class="legend-color" style="background: orange;"></span>Auth</div>
        <div class="legend-item"><span class="legend-color" style="background: green;"></span>User</div>
        <div class="legend-item"><span class="legend-color" style="background: purple;"></span>File</div>
        <div class="legend-item"><span class="legend-color" style="background: gray;"></span>General</div>
    </div>
    <script>
        var nodes_data = """ + self.to_json() + """;
        
        var colors = {
            'admin': 'red', 'api': 'blue', 'auth': 'orange',
            'user': 'green', 'file': 'purple', 'general': 'gray'
        };
        
        var nodes = new vis.DataSet(nodes_data.nodes.map(function(node) {
            return {
                id: node.id,
                label: node.path || '/',
                title: node.url,
                color: colors[node.type] || 'gray',
                shape: node.type === 'admin' ? 'star' : 'box'
            };
        }));
        
        var edges = new vis.DataSet(nodes_data.edges.map(function(edge, i) {
            return {
                id: i,
                from: edge.source,
                to: edge.target,
                arrows: 'to'
            };
        }));
        
        var container = document.getElementById('graph');
        var data = { nodes: nodes, edges: edges };
        var options = {
            physics: { enabled: true, stabilization: true },
            layout: { hierarchical: false }
        };
        
        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>"""
        return html
    
    def save_graph(self, output_path: str, format: str = "json"):
        """Save graph to file"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "json":
            content = self.to_json()
        elif format == "dot":
            content = self.to_dot()
        elif format == "gexf":
            content = self.to_gexf()
        elif format == "html":
            content = self.to_html()
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        path.write_text(content)
        return path
