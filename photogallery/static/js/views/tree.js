function TreeItem(aId, aOnSelected) {
	var self = this;

	self.myId = aId;
	self.myOnSelected = aOnSelected;

	// Public members
	self.iconClass = ko.observable();
	self.label = ko.observable();
	self.tooltip = ko.observable();
	self.value = ko.observable();

	// Private members
	self.myIsSelected = ko.observable(false);
	self.myItems = ko.observableArray();

	self.myIsExpanded = ko.pureComputed(function myIsExpanded() {
		return self.myIsSelected() || self.hasSelectedItem();
	});

	self.hasSelectedItem = function hasActiveChild() {
		for (var i = 0; i < self.myItems().length; i++) {
			var child = self.myItems()[i];

			if (child.myIsSelected() || child.hasSelectedItem()) {
				return true;
			}
		}

		return false;
	};

	self.select = function() {
		if (self.myOnSelected) {
			self.myOnSelected(self);	
		}
	};


	self.selectById = function(aId) {
		self.myIsSelected(aId == self.myId);
		
		for (var i = 0; i < self.myItems().length; i++) {
			self.myItems()[i].selectById(aId);
		}

		if (!self.myIsSelected()) {
			return;
		}

		if (self.myOnSelected) {
			self.myOnSelected(self);	
		}
	};

	self.addItem = function(aItem) {
		self.myItems.push(aItem);
	};
};