function Route() {
	var self = this;

	self.myRoutes = [];

	self.route = function route(aUrl) {
		for (var i = 0; i < self.myRoutes.length; i++) {
			var route = self.myRoutes[i];
			
			var matches = aUrl.match(route[0]);
			if (matches) {
				route[1](matches);
			}
		}
	};

	self.add = function push(aRoute) {
		self.myRoutes.push(aRoute);
	};
};