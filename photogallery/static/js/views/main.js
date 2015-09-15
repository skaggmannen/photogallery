function MainView(aData, aRoute) {
	var self = this;

	self.myData = aData;

	self.mySidebarView = new SidebarView(aData);
	self.myContentView = new ContentView(aData);

	var routeAll = function(aMatches) {
		self.mySidebarView.selectAll();

		var selectedDate = self.myData.mySelectedDate();
		if (selectedDate != undefined) {
			self.myData.mySelectedDate(undefined);	
		}

		self.myContentView.showGallery();
	};

	var routeYear = function(aMatches) {
		var year = parseInt(aMatches[1]);

		self.mySidebarView.selectYear(year);


		var selectedDate = self.myData.mySelectedDate();
		if (!selectedDate || year != selectedDate.myYear || selectedDate.myMonth != undefined) {
			self.myData.mySelectedDate({
				myYear: year,
			});
		}

		self.myContentView.showGallery();
	};

	var routeMonth = function(aMatches) {
		var year = parseInt(aMatches[1]);
		var month = parseInt(aMatches[2]);

		self.mySidebarView.selectMonth(year, month);

		var selectedDate = self.myData.mySelectedDate();
		if (!selectedDate || year != selectedDate.myYear || month != selectedDate.myMonth) {
			self.myData.mySelectedDate({
				myYear: year,
				myMonth: month,
			});
		}

		self.myContentView.showGallery();
	};

	var routeImage = function(aMatches) {
		var imageId = aMatches[1];

		self.myContentView.showImage(imageId);
	};

	var routeTrash = function(aMatches) {
		self.mySidebarView.selectTrash();
		self.myContentView.showTrash();
	};

	aRoute.add([/^\/all$/, 						routeAll]);
	aRoute.add([/^\/all\/(\d{4})$/,				routeYear]);
	aRoute.add([/^\/all\/(\d{4})-(\d{1,2})$/, 	routeMonth]);
	aRoute.add([/^\/image\/(.+)$/,				routeImage]);
	aRoute.add([/^\/trash$/, 					routeTrash]);
};