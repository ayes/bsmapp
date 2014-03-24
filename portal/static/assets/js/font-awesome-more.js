(function() {
	var ICONS;

	var icon = function(id) {
		return '<i class="icon-' + id + '"></i>';
	}

	var shortcode = function(id) {
		return '[icon name="icon-' + id + '"]';
	}

	var createControl = function(name, controlManager) {
		if (name != 'fontAwesomeMoreGlyphSelect') return null;
		var listBox = controlManager.createListBox('fontAwesomeMoreGlyphSelect', {
			title: 'Glyphs',
			onselect: function(v) {
				var editor = this.control_manager.editor;
				if (v) {
					editor.selection.setContent(shortcode(v));
				}		
				return false;
			}
		});

		for (var i = 0; i < ICONS.length; i++) {
			var _id = ICONS[i];
			listBox.add(icon(_id) + ' ' + _id, _id);
		}

		return listBox;
	};

	tinymce.create('tinymce.plugins.FontAwesomeMoreGlyphPlugin', {
		createControl: createControl
	});

	tinymce.PluginManager.add('font_awesome_more_glyphs', tinymce.plugins.FontAwesomeMoreGlyphPlugin);

	ICONS = ["accessibility-sign", "adjust", "adn", "adobe-pdf", "align-center", "align-justify", "align-left", "align-right", "amazon", "amazon-sign", "ambulance", "anchor", "android", "angle-down", "angle-left", "angle-right", "angle-up", "apple", "apple-itunes", "archive", "arrow-down", "arrow-left", "arrow-right", "arrow-up", "asterisk", "aws", "backward", "ban-circle", "bar-chart", "barcode", "beaker", "beer", "bell", "bell-alt", "bike-sign", "bing", "bing-sign", "bitbucket", "bitbucket-sign", "bitcoin", "blogger", "blogger-sign", "bold", "bolt", "book", "bookmark", "bookmark-empty", "briefcase", "bug", "building", "bullhorn", "bullseye", "bus-sign", "calendar", "calendar-empty", "camera", "camera-retro", "car-sign", "caret-down", "caret-left", "caret-right", "caret-up", "certificate", "check", "check-minus", "check-sign", "chevron-down", "chevron-left", "chevron-right", "chevron-sign-down", "chevron-sign-left", "chevron-sign-right", "chevron-sign-up", "chevron-up", "chrome", "circle", "circle-arrow-down", "circle-arrow-left", "circle-arrow-right", "circle-arrow-up", "circle-blank", "cloud", "cloud-download", "cloud-upload", "code", "code-fork", "coffee", "collapse", "collapse-alt", "collapse-top", "columns", "comment", "comment-alt", "comments", "comments-alt", "compass", "copy", "credit-card", "crop", "css3", "css3-more", "cut", "dashboard", "delicious", "desktop", "dollar", "double-angle-down", "double-angle-left", "double-angle-right", "double-angle-up", "download", "download-alt", "dribbble", "dribbble-sign", "dropbox", "drupal", "duck-duck-go", "edit", "edit-sign", "eject", "ellipsis-horizontal", "ellipsis-vertical", "envelope", "envelope-alt", "eraser", "euro", "evernote", "evernote-sign", "exchange", "exclamation", "exclamation-sign", "expand", "expand-alt", "external-link", "external-link-sign", "eye-close", "eye-open", "facebook", "facebook-sign", "facetime-video", "fast-backward", "fast-forward", "female", "fighter-jet", "file", "file-alt", "file-text", "file-text-alt", "film", "filter", "fire", "fire-extinguisher", "firefox", "flag", "flag-alt", "flag-checkered", "flickr", "flickr-more", "folder-close", "folder-close-alt", "folder-open", "folder-open-alt", "font", "food", "forrst", "forrst-sign", "forward", "foursquare", "foursquare-more", "frown", "fullscreen", "gamepad", "gbp", "gear", "gears", "gift", "git-fork", "github", "github-alt", "github-sign", "gittip", "glass", "globe", "google", "google-plus", "google-plus-sign", "google-sign", "group", "h-sign", "hacker-news", "hand-down", "hand-left", "hand-right", "hand-up", "hdd", "headphones", "heart", "heart-empty", "home", "hospital", "html5", "ie", "inbox", "indent-left", "indent-right", "info", "info-sign", "instagram", "instagram-more", "italic", "key", "keyboard", "laptop", "lastfm", "lastfm-sign", "layers", "leaf", "legal", "lemon", "level-down", "level-up", "lightbulb", "link", "linkedin", "linkedin-sign", "linux", "list", "list-alt", "list-ol", "list-ul", "location-arrow", "lock", "long-arrow-down", "long-arrow-left", "long-arrow-right", "long-arrow-up", "magic", "magnet", "mail-forward", "mail-reply", "mail-reply-all", "male", "map", "map-marker", "maxcdn", "medkit", "meh", "microphone", "microphone-off", "minus", "minus-sign", "minus-sign-alt", "mobile-phone", "money", "moon", "move", "ms-excel", "ms-ppt", "ms-word", "music", "ok", "ok-circle", "ok-sign", "opera", "paperclip", "paste", "pause", "paypal", "pencil", "phone", "phone-sign", "picasa", "picasa-sign", "picture", "pinterest", "pinterest-sign", "plane", "play", "play-circle", "play-sign", "plus", "plus-sign", "plus-sign-alt", "power-off", "print", "pushpin", "puzzle-piece", "qrcode", "question", "question-sign", "quote-left", "quote-right", "random", "reddit", "refresh", "remove", "remove-circle", "remove-sign", "renminbi", "renren", "reorder", "reply-all", "resize-full", "resize-horizontal", "resize-small", "resize-vertical", "retweet", "road", "rocket", "rotate-left", "rotate-right", "rss", "rss-sign", "rupee", "safari", "save", "screenshot", "search", "share", "share-sign", "share-this", "share-this-sign", "shield", "shopping-cart", "sign-blank", "signal", "signin", "signout", "sitemap", "skype", "skype", "smile", "sort", "sort-by-alphabet", "sort-by-alphabet-alt", "sort-by-attributes", "sort-by-attributes-alt", "sort-by-order", "sort-by-order-alt", "sort-down", "sort-up", "soundcloud", "sparrow", "sparrow-sign", "spinner", "spotify", "stack-overflow", "stackexchange", "star", "star-empty", "star-half", "star-half-full", "step-backward", "step-forward", "stethoscope", "stop", "strikethrough", "subscript", "suitcase", "sun", "superscript", "table", "tablet", "tag", "tags", "tasks", "taxi-sign", "terminal", "text-height", "text-width", "th", "th-large", "th-list", "thumbs-down", "thumbs-down-alt", "thumbs-up", "thumbs-up-alt", "ticket", "time", "tint", "trash", "trello", "trophy", "truck", "truck-sign", "tumblr", "tumblr-sign", "twitter", "twitter-sign", "umbrella", "unchecked", "underline", "unlink", "unlock", "unlock-alt", "upload", "upload-alt", "user", "user-md", "vimeo", "vimeo-sign", "vk", "volume-down", "volume-off", "volume-up", "warning-sign", "weibo", "windows", "windows-more", "won", "wordpress", "wordpress-sign", "wrench", "xing", "xing-sign", "yahoo", "yelp", "yelp-sign", "yen", "youtube", "youtube-play", "youtube-sign", "zip-file", "zoom-in", "zoom-out"];
})();