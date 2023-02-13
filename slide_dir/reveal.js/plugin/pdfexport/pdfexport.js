var PdfExport = ( function( Reveal ){

	var defMode = false;

	function getRevealJsPath(){
		var regex = /\/js\/reveal.js$/i;
		var script = Array.from( document.querySelectorAll( 'script' ) ).find( function( e ){
			return e.attributes.src && e.attributes.src.value.search( regex ) >= 0;
		});
		if( !script ){
			console.error( 'reveal.js script could not be found in included <script> elements. Did you rename this file?' );
			return '';
		}
		return script.attributes.src.value.replace( regex, '' );
	}

	function setStylesheet( pdf ){
		var link = document.querySelector( '#print' );
		if( !link ){
			link = document.createElement( 'link' );
			link.rel = 'stylesheet';
			link.id = 'print';
			document.querySelector( 'head' ).appendChild( link );
		}
		var style = 'paper';
		if( pdf ){
			style = 'pdf';
		}
		link.href = getRevealJsPath() + '/css/print/' + style + '.css';
	}

	function setPdfExport( pdfExport ){
		var config = Reveal.getConfig();
		pdfExport = pdfExport !== null ? pdfExport : config.pdfExport !== undefined ? !!config.pdfExport : defMode;
		setStylesheet( pdfExport );
	}

	function isPrintingPDF(){
		return ( /print-pdf/gi ).test( window.location.search );
	}

	function togglePdfExport(){
		var url_doc = new URL( document.URL );
		var query_doc = new URLSearchParams( url_doc.searchParams );
		if( isPrintingPDF() ){
			query_doc.delete( 'print-pdf' );
		}else{
			query_doc.set( 'print-pdf', '' );
		}
		url_doc.search = ( query_doc.toString() ? '?' + query_doc.toString() : '' );
		window.location.href = url_doc.toString();
	}

	function applyPdfExportParameter(){
		setPdfExport( isPrintingPDF() );
	}

	function installKeyBindings(){
		var config = Reveal.getConfig();
		var shortcut = config.pdfExportShortcut || 'E';
		if( !config.keyboard ){
			return;
		}
		var keyboard = config.keyboard === true ? {} : config.keyboard;
		keyboard[ shortcut.toUpperCase().charCodeAt( 0 ) ] = togglePdfExport;

		Reveal.registerKeyboardShortcut( shortcut, 'PDF export mode' );
		Reveal.configure({
			keyboard: keyboard
		});
	}

	function install(){
		installKeyBindings();
		applyPdfExportParameter();
	}

	install();

	return {
	};

})( Reveal );
