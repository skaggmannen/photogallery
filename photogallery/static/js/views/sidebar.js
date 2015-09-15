var MONTH_NAMES = {
	1: "Januari",
	2: "Februari",
	3: "Mars",
	4: "April",
	5: "Maj",
	6: "Juni",
	7: "Juli",
	8: "Augusti",
	9: "September",
	10: "Oktober",
	11: "November",
	12: "December",
};

function SidebarView(aData) {
	var self = this;

	self.myData = aData;

	self.myYears = {};
	self.myMonths = {};
	self.myAll = undefined;

	self.myIsExpanded = ko.observable(false);
	self.mySelectedId = undefined;

	// Private members
	function onAll(aItem) {
		var hash = "#/all";
		if (hash == window.location.hash) {
			return;
		}

		window.location.hash = hash;
	}

	function onYear(aItem) {
		var hash = "#/all/" + aItem.value().myYear;

		if (hash == window.location.hash) {
			return;
		}

		window.location.hash = hash;
	};

	function onMonth(aItem) {
		var hash = "#/all/" + aItem.value().myYear + "-" + aItem.value().myMonth;

		if (hash == window.location.hash) {
			return;
		}

		window.location.hash = hash;
	};

	function onTrash(aItem) {
		var hash = "#/trash";

		if (hash == window.location.hash) {
			return;
		}

		window.location.hash = hash;
	};

	function createAllItem() {
		var allItem = new TreeItem("all", onAll);
		allItem.label("Alla bilder");
		allItem.iconClass("glyphicon glyphicon-calendar")

		var dates = self.myData.myDates().sort(function(aFirst, aSecond) {
			if (aFirst["year"] == aSecond["year"]) {
				return aFirst["month"] - aSecond["month"];
			}

			return aFirst["year"] - aSecond["year"];
		});

		// Map month items to years
		var months = {};
		for (var i = 0; i < dates.length; i++) {
			var date = dates[i];
			var year = date["year"];
			var month = date["month"];
			var count = date["count"];

			if (months[year] == undefined) {
				months[year] = [];
			}

			var item = new TreeItem("all-" + year + month, onMonth);
			item.label(MONTH_NAMES[month]);
			item.value({myYear: year, myMonth: month, myCount: count});
			item.tooltip("Antal: " + count);

			if (!self.myMonths[year]) {
				self.myMonths[year] = {};
			}
			self.myMonths[year][month] = item;

			months[year].push(item);
		}

		// Create year items
		for (var year in months) {
			var item = new TreeItem("all-" + year, onYear);
			item.label(year);
			item.value({myYear: year});

			var total = 0;
			for (var i = 0; i < months[year].length; i++) {
				var monthItem = months[year][i];

				if (monthItem.value().myCount) {
					total += monthItem.value().myCount;
				}

				item.addItem(monthItem);
			}

			item.tooltip("Antal: " + total);

			self.myYears[year] = item;

			allItem.addItem(item);
		}

		return allItem;
	};

	function createTrashItem() {
		var trashItem = new TreeItem("trash", onTrash);
		trashItem.label("Papperskorg");
		trashItem.iconClass("glyphicon glyphicon-trash")

		return trashItem;
	};

	self.myTreeView = ko.computed(function myTreeView() {
		var root = new TreeItem("root");

		root.addItem(createAllItem());
		root.addItem(createTrashItem());

		root.selectById(self.mySelectedId);

		return root;
	});

	self.toggle = function() {
		self.myIsExpanded(!self.myIsExpanded());
	};

	self.selectAll = function() {
		self.mySelectedId = "all";
		self.myTreeView().selectById(self.mySelectedId);
	};

	self.selectYear = function(aYear) {
		self.mySelectedId = "all-" + aYear;
		self.myTreeView().selectById(self.mySelectedId);
	};

	self.selectMonth = function(aYear, aMonth) {
		self.mySelectedId = "all-" + aYear + aMonth;
		self.myTreeView().selectById(self.mySelectedId);
	};

	self.selectTrash = function() {
		self.mySelectedId = "trash";
		self.myTreeView().selectById(self.mySelectedId);
	};
}