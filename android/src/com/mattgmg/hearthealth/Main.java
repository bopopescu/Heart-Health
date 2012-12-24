package com.mattgmg.hearthealth;

import android.net.Uri;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.TextView;
import android.app.Activity;
import android.content.Intent;

public class Main extends Activity {
	
    private String mLastUrl = "http://www.hearthealthapp.com/";
    private boolean mErrorOccurred = false;
    private boolean mContentLoaded = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        final WebView webView = (WebView)findViewById(R.id.webview);
        final Button tryAgainButton = (Button)findViewById(R.id.try_again_button);
    	final TextView statusText = (TextView)findViewById(R.id.status_text);
    	final View loadingLayout = findViewById(R.id.loading_layout);
    	final View progressBar = findViewById(R.id.progress_bar);
    	
    	webView.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
    	
    	webView.setWebViewClient(new WebViewClient() {  
	        @Override  
	        public boolean shouldOverrideUrlLoading(WebView view, String url)  
	        {  
        		view.setVisibility(View.GONE);
        		loadingLayout.setVisibility(View.VISIBLE);
        		statusText.setVisibility(View.GONE);
        		progressBar.setVisibility(View.VISIBLE);
        		tryAgainButton.setVisibility(View.GONE);
            	
	        	Uri uri = Uri.parse(url);
	        	if(uri.isRelative() || url.contains("hearthealthapp")){
	        		mLastUrl = url;
			        view.loadUrl(url);  
	        	} else {
	        		Intent browserIntent = new Intent(Intent.ACTION_VIEW, uri);
	        		startActivity(browserIntent);
	        	}
		        return true;  
	        }

			@Override
			public void onReceivedError(WebView view, int errorCode,
					String description, String failingUrl) {
				super.onReceivedError(view, errorCode, description, failingUrl);
        		webView.setVisibility(View.GONE);
            	loadingLayout.setVisibility(View.VISIBLE);
            	tryAgainButton.setVisibility(View.VISIBLE);
            	progressBar.setVisibility(View.GONE);
            	statusText.setVisibility(View.VISIBLE);
            	statusText.setText("Unable to load. Please make sure you are connected to the internet and try again.");
            	mLastUrl = failingUrl;
            	mErrorOccurred = true;
			}  
			
            public void onPageFinished(WebView view, String url) {
            	if(!mErrorOccurred){
	            	loadingLayout.setVisibility(View.GONE);
	            	webView.setVisibility(View.VISIBLE);
	            	mContentLoaded = true;
            	}
            }
	      }); 
    	
    	// Enable location within the webview
		webView.setWebChromeClient(new WebChromeClient() {
			public void onGeolocationPermissionsShowPrompt(String origin, android.webkit.GeolocationPermissions.Callback callback) {
			   callback.invoke(origin, true, false);
			}
		});
	   
    	webView.getSettings().setGeolocationDatabasePath("/data/data/hearthealth/");
	    webView.getSettings().setBuiltInZoomControls(true);
	    webView.getSettings().setJavaScriptEnabled(true);
	    webView.getSettings().setDomStorageEnabled(true);
    	
    	webView.setOnTouchListener(new View.OnTouchListener() { 
    		@Override
    		public boolean onTouch(View v, MotionEvent event) {
    		           switch (event.getAction()) { 
    		               case MotionEvent.ACTION_DOWN: 
    		               case MotionEvent.ACTION_UP: 
    		                   if (!v.hasFocus()) { 
    		                       v.requestFocus(); 
    		                   } 
    		                   break; 
    		           } 
    		           return false; 
    		        }
		});
    	
    	if(!mContentLoaded && savedInstanceState == null){
	    	webView.loadUrl(mLastUrl);
    	}
    }
    
    @Override
    protected void onSaveInstanceState(Bundle outState )
    {
	    super.onSaveInstanceState(outState);
        WebView webView = (WebView)findViewById(R.id.webview);
        webView.saveState(outState);
	    outState.putString("url", mLastUrl);
	    
    }

    @Override
    protected void onRestoreInstanceState(Bundle savedInstanceState)
    {
	    super.onSaveInstanceState(savedInstanceState);
	    if(savedInstanceState != null){
		    mLastUrl = savedInstanceState.getString("url");
	        WebView webView = (WebView)findViewById(R.id.webview);
	        webView.restoreState(savedInstanceState);
	    }
    }
    
    public void onTryAgainClicked(View v){
    	mErrorOccurred = false;
		findViewById(R.id.status_text).setVisibility(View.GONE);
		findViewById(R.id.progress_bar).setVisibility(View.VISIBLE);
		v.setVisibility(View.GONE);
		WebView webView = (WebView)findViewById(R.id.webview);
    	webView.loadUrl(mLastUrl);
    }
    
    
    
}
