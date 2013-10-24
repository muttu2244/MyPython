package zynga.greyhound.client.test
{
	import flash.display.Loader;
	import flash.display.LoaderInfo;
	import flash.display.Sprite;
	import flash.display.Stage;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.net.URLRequest;
	import flash.system.LoaderContext;
	import flash.system.Security;
	import flash.utils.ByteArray;
	import flash.utils.Dictionary;
	import flash.utils.describeType;
	
	import mx.controls.Alert;
	
	import spark.components.Button;
	
	import zynga.greyhound.client.base.Constants;
	import zynga.greyhound.client.base.ErrorCodes;
	import zynga.greyhound.client.base.IGame;
	import zynga.greyhound.client.base.IGraph;
	import zynga.greyhound.client.base.IGreyhound;
	import zynga.greyhound.client.base.ITime;
	
	public class UserGraphUIMgr
	{
		private var m_ui:Object;
		private var m_greyhound:IGreyhound;
		
		
		public function UserGraphUIMgr(greyhound:IGreyhound, uiControls:Object)
		{
			m_greyhound = greyhound;
			m_ui = uiControls;
			initHandlers();
		}
		public function removeHandlers():void
		{
			m_ui.getGraphBtn.removeEventListener(MouseEvent.CLICK, getGraphBtnhand);
			m_greyhound = null;
			m_ui = null;
		}
		public function updateGraphField(status : Object, params : Object) : void
		{
			if(status.error === ErrorCodes.SUCCESS) {
				m_ui.displayGraph.text = JSON.stringify(params.data);
			} else {
				m_ui.displayGraph.text = "Failed to get data: status=" + JSON.stringify(status) + " params=" + JSON.stringify(params);
			}
		}
		
		/**
		 * Trim leading and trailing spaces from a string
		 * @method trim
		 * @return {String} Trimmed string
		 */
		public function trim(s:String):String 
		{
			return s.replace(/^\s+|\s+$/g, '');
		};
		
		public function refreshGraphDisplay():void
		{
			m_ui.displayGraph.text = "Fetching...";
			m_greyhound.graph.getGraphMembers([ "app-friend" ], updateGraphField);
		}
		private function getGraphBtnhand(e:MouseEvent):void
		{
			refreshGraphDisplay();
		}
		public function initHandlers():void
		{
			m_ui.getGraphBtn.addEventListener(MouseEvent.CLICK, getGraphBtnhand);
		}
	}
}
