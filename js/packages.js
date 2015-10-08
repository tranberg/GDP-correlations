(function() {
    packages = {

        // Lazily construct the package hierarchy from class names.
        root: function(classes) {
            var map = {};

            function find(name, data) {
                var node = map[name],
                    i;
                if (!node) {
                    node = map[name] = data || {
                        name: name,
                        children: []
                    };
                    if (name.length) {
                        node.parent = find(name.substring(0, i =
                            name.lastIndexOf(".")));
                        node.parent.children.push(node);
                        node.key = name.substring(i + 1);
                    }
                }
                return node;
            }

            classes.forEach(function(d) {
                find(d.name, d);
            });

            return map[""];
        },

        // Return a list of connections for the given array of nodes.
        connections: function(nodes) {
            var map = {},
                connections = [];

            // Compute a map from name to node.
            nodes.forEach(function(d) {
                map[d.name] = d;
            });

            // For each connection, construct a link from the source to target node.
            nodes.forEach(function(d) {
                if (d.connections) Object.keys(d.connections).forEach(
                        function(i) {
                            connections.push({
                                source: map[d.name],
                                target: map[i],
                                strength: {"key": d.connections[i]}
                            });
                        });
            });

            return connections;
        }

    };
})();
