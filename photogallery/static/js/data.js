function Image() {
	var self = this;

	self.myId = ko.observable();
	self.myUrl = ko.observable();
	self.myOrientation = ko.observable();
	self.myThumbUrl = ko.observable();
	self.myIsLoaded = ko.observable(false);
	self.myFillWidth = ko.observable(false);
	self.myFillHeight = ko.observable(true);

	self.myOnLoad = function(aImage, aEvent) {
		self.myIsLoaded(true);

		var target = $(aEvent.target);
		var width = target.width();
		var height = target.height();
		if (width > height)
		{
			self.myFillHeight(true);
			self.myFillWidth(false);
		}
		else
		{
			self.myFillHeight(false);
			self.myFillWidth(true);
		}
	};
};

function Data() {
	var self = this;

	self.myDates = ko.observableArray([]);
	self.mySelectedDate = ko.observable();

	self.myImages = undefined;
	self.myImageCache = {};

	function getQuery(aSelectedDate, aOffset, aCount)
	{
		var year = undefined;
		var month = undefined;

		if (aSelectedDate !== undefined)
		{
			year = self.mySelectedDate().myYear;
			month = self.mySelectedDate().myMonth;
		}

		if (!aOffset && !aCount && !year && !month)
		{
			return "";
		}

		var query = "?";
		if (aOffset !== undefined)
		{
			query += "offset=" + aOffset + "&";
		}

		if (aCount !== undefined)
		{
			query += "limit=" + aCount + "&";
		}

		if (year !== undefined)
		{
			query += "year=" + year + "&";	
		}
		
		if (month !== undefined)
		{
			query += "month=" + month + "&";
		}

		return query;
	}

	self.myImageResource = ko.computed(function myImageResource() {
		var selectedDate = self.mySelectedDate();

		self.myImages = undefined;

		return {
			get: function (aOffset, aCount) {
				var deferred = $.Deferred();
				var images = self.myImages;

				if (images === undefined)
				{
					deferred.resolve([]);
					return deferred.promise();
				}

				// If offset is outside available images, return empty array
				if (aOffset >= images.length)
				{
					deferred.resolve([]);
					return deferred.promise();
				}

				// Check if all images in range has been requested
				var dirty = false;
				for (var i = aOffset; !dirty && i < aOffset + aCount; i++)
				{
					if (i >= images.length)
					{
						break;
					}

					dirty = images[i] == undefined;
				}

				if (dirty)
				{
					// Pre-populate a larger range so we don't fetch multiple times
					for (var i = aOffset; i < aOffset + aCount * 3; i++)
					{
						if (i >= images.length)
						{
							break;
						}
						images[i] = new Image();
					}

					$.get("/api/v1/photo/" + getQuery(selectedDate, aOffset, aCount * 3))
						.done(function getImagesDone(aData)
						{
							for (var i = 0; i < aData.photos.length; i++)
							{
								if (aOffset + i >= images.length)
								{
									images.push(new Image());
								}
								
								images[aOffset + i].myId(aData.photos[i].id);
								images[aOffset + i].myUrl(aData.photos[i].url);
								images[aOffset + i].myOrientation(aData.photos[i].orientation);
								images[aOffset + i].myThumbUrl(aData.photos[i].thumb);
							}
						});
				}

				deferred.resolve(images.slice(aOffset, aOffset + aCount));

				return deferred.promise();
			},
			getCount: function () {
				var deferred = $.Deferred();

				if (self.myImages !== undefined)
				{
					deferred.resolve(self.myImages.length);
					return deferred.promise();
				}

				$.get("/api/v1/photo/" + getQuery(selectedDate))
					.done(function getCountDone(aData)
					{
						self.myImages = new Array(aData.total_count);

						for (var i = 0; i < aData.photos.length; i++)
						{
							image = new Image();
							image.myId(aData.photos[i].id);
							image.myUrl(aData.photos[i].url);
							image.myOrientation(aData.photos[i].orientation);
							image.myThumbUrl(aData.photos[i].thumb);

							self.myImages[i] = image;
						}

						deferred.resolve(aData.total_count);
					});

				return deferred.promise();
			},
		};
	});

	self.getImage = function getImage(aImageId)
	{
		if (self.myImageCache[aImageId] === undefined)
		{
			self.myImageCache[aImageId] = new Image();
			self.myImageCache[aImageId].myId(aImageId);

			$.get("/api/v1/photo/" + aImageId)
				.done(function getImageDone(aData)
				{
					self.myImageCache[aImageId].myUrl(aData.url);
					self.myImageCache[aImageId].myThumbUrl(aData.thumb);
				});
		}

		return self.myImageCache[aImageId];
	};

	self.getDates = function getDates()
	{
		$.get("/api/v1/date/")
			.done(function getDatesDone(aData)
			{
				self.myDates(aData.dates);
			});
	};
}