package com.mattgmg.hearthealth;

import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.app.Activity;

public class Main extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        final WebView webView = (WebView)findViewById(R.id.webview);
    	
    	webView.setWebViewClient(new WebViewClient() {  
	        @Override  
	        public boolean shouldOverrideUrlLoading(WebView view, String url)  
	        {  
	          view.loadUrl(url);  
	          return true;  
	        }

			@Override
			public void onReceivedError(WebView view, int errorCode,
					String description, String failingUrl) {
				super.onReceivedError(view, errorCode, description, failingUrl);
			}  
			
            public void onPageFinished(WebView view, String url) {
            	findViewById(R.id.loading_layout).setVisibility(View.GONE);
            	webView.setVisibility(View.VISIBLE);
            }
	        
	      }); 
	    
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
    	
    	webView.loadUrl("http://www.hearthealthapp.com/");
    }
    
    
    
}
