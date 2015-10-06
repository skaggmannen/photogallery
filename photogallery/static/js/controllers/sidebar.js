var sidebarModule = angular.module('SidebarModule', [])

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

sidebarModule.controller('Sidebar', ['$scope', '$http',
	function($scope, $http) {

		$scope.collapsed = true;
		$scope.selectedItem = undefined;

		$scope.toggle = function toggle() {
			$scope.collapsed = !$scope.collapsed;
		};

		function onItemSelected(item) {
			$scope.allItem.selectById(item.id);
		};

		function buildDateTree(dates) {
			var sortedDates = dates.sort(function(first, second) {
				if (first.year == second.year) {
					return first.month - second.month;
				}

				return first.year - second.year;
			});

			// Map month items to years
			var months = {};
			for (var i = 0; i < dates.length; i++) {
				var date = dates[i];
				var year = date.year;
				var month = date.month;

				if (months[year] == undefined) {
					months[year] = [];
				}

				var item = new TreeItem();
				item.id = "all-" + year + "-" + month;
				item.label = MONTH_NAMES[month];
				item.value = date;
				item.onSelected = onItemSelected;

				months[year].push(item);
			}

			// Create year items
			var years = [];
			for (var year in months) {
				var item = new TreeItem();
				item.id = "all-" + year;
				item.label = year;
				item.value = { year: year };
				item.onSelected = onItemSelected;

				for (var i = 0; i < months[year].length; i++) {
					var monthItem = months[year][i];
					item.children.push(monthItem);
				}

				years.push(item)
			}

			return years;
		};

		function getDates() {
			var allItem = new TreeItem();
			allItem.id = "all";
			allItem.label = "Alla bilder";
			allItem.children = [];
			allItem.onSelected = onItemSelected;

			$scope.allItem = allItem;

			$http.get("/api/v1/date/").success(function getDatesDone(data) {
				angular.copy(buildDateTree(data.dates), allItem.children);
			});
		};

		getDates();
	}
]);