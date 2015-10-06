var treeModule = angular.module("TreeModule", []);

function TreeItem() {
	var self = this;

	self.id = undefined;
	self.label = undefined;
	self.value = undefined;
	self.onSelected = undefined;

	self.isSelected = false;
	self.children = [];

	self.hasSelectedChild = function hasSelectedChild() {
		for (var i = 0; i < self.children.length; i++) {
			var child = self.children[i];

			if (child.isExpanded()) {
				return true;
			}
		}

		return false;
	};

	self.isExpanded = function isExpanded() {
		return self.isSelected || self.hasSelectedChild();
	};

	self.select = function select() {
		self.isSelected = true;
		if (self.onSelected) {
			self.onSelected(self);
		}
	};

	self.selectById = function selectById(id) {
		self.isSelected = self.id == id;

		for (var i = 0; i < self.children.length; i++) {
			self.children[i].selectById(id);
		}
	};
}

treeModule.directive("tree", ['RecursionHelper', function (RecursionHelper) {
	return {
		restrict: 'E',
		scope: {
			item: '=item'
		},
		templateUrl: "/static/partials/tree.html",
		compile: function(element) {
			return RecursionHelper.compile(element);
		}
	}
}]);