import d from"https://cdn.jsdelivr.net/npm/@flourish/live-api@5.1.0/+esm";function n({model:e,el:i}){let t=document.createElement("div");t.id="chart",i.appendChild(t);let a=e.get("_model_data");a.base_visualisation_id&&(a.base_visualisation_id=String(a.base_visualisation_id),a.bindings=a.base_bindings,a.data=a.base_data,a.metadata=a.base_metadata,a.state={...a.base_state,...a.state}),a.base_visualisation_id&&a.data!==null&&(a.data=a.data,a.bindings=a.bindings),(a.metadata!==null||typeof a.metadata<"u")&&(a.metadata=a.metadata||a.base_metadata),a.container=t,flourish_visualisation=new d.Live(a),a.base_visualisation_id&&!flourish_visualisation.template_loaded&&(flourish_visualisation.template_loaded=!0)}var r=()=>({render:n});export{r as default};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsiLi4vLi4vanMvd2lkZ2V0LnRzIl0sCiAgInNvdXJjZXNDb250ZW50IjogWyJpbXBvcnQgdHlwZSB7IFJlbmRlckNvbnRleHQgfSBmcm9tIFwiQGFueXdpZGdldC90eXBlc1wiO1xuaW1wb3J0IFwiLi93aWRnZXQuY3NzXCI7XG5cbmltcG9ydCBmbG91cmlzaGxpdmVBcGkgZnJvbSAnaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9AZmxvdXJpc2gvbGl2ZS1hcGlANS4xLjAvK2VzbSdcblxuaW50ZXJmYWNlIFdpZGdldE1vZGVsIHtcblx0X21vZGVsX2RhdGE6IHtcblx0XHRjb250YWluZXI6IEhUTUxFbGVtZW50XG5cdH1cbn1cblxuZnVuY3Rpb24gcmVuZGVyKHsgbW9kZWwsIGVsIH06IFJlbmRlckNvbnRleHQ8V2lkZ2V0TW9kZWw+KSB7XG5cblx0bGV0IGNoYXJ0ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTsgXG5cdGNoYXJ0LmlkID0gXCJjaGFydFwiO1xuXHRlbC5hcHBlbmRDaGlsZChjaGFydCk7XG5cdGxldCBvcHRzID0gbW9kZWwuZ2V0KFwiX21vZGVsX2RhdGFcIik7XG5cdGlmIChvcHRzLmJhc2VfdmlzdWFsaXNhdGlvbl9pZCkge1xuXHRcdC8vIGJhc2VfdmlzdWFsaXNhdGlvbl9kYXRhX2Zvcm1hdCBjYW4gbm93IGJlIGFuIGFycmF5IG9mIGFycmF5cyBvciBhcnJheSBvZiBvYmplY3RzIGFzIHY1LjAuMiBvZiB0aGUgQVBJLlxuXHRcdG9wdHMuYmFzZV92aXN1YWxpc2F0aW9uX2lkID0gU3RyaW5nKG9wdHMuYmFzZV92aXN1YWxpc2F0aW9uX2lkKVxuXHRcdG9wdHMuYmluZGluZ3MgPSBvcHRzLmJhc2VfYmluZGluZ3Ncblx0XHRvcHRzLmRhdGEgPSBvcHRzLmJhc2VfZGF0YVxuXHRcdG9wdHMubWV0YWRhdGEgPSBvcHRzLmJhc2VfbWV0YWRhdGFcblx0XHQvLyBtZXJnZSB0aGUgdHdvIHN0YXRlcyB0b2dldGhlci4gSWYgdGhlcmUgaXMgYSByZXBsYWNlbWVudCB2YWx1ZSBmb3IgYSBrZXkgaW4gb3B0cy5iYXNlX3N0YXRlLCByZXBsYWNlIHdpdGggdGhlIHZhbHVlIGluIG9wdHMuc3RhdGUgKHNldCBpbiB0aGUgUi9QeXRob24gY29kZSlcblx0XHRvcHRzLnN0YXRlID0geyAuLi5vcHRzLmJhc2Vfc3RhdGUsIC4uLm9wdHMuc3RhdGUgfVxuXHQgIH1cblx0ICBpZiAob3B0cy5iYXNlX3Zpc3VhbGlzYXRpb25faWQgJiYgb3B0cy5kYXRhICE9PSBudWxsKXtcblx0XHRvcHRzLmRhdGEgPSBvcHRzLmRhdGFcblx0XHRvcHRzLmJpbmRpbmdzID0gb3B0cy5iaW5kaW5nc1xuXHQgIH1cblx0ICBpZihvcHRzLm1ldGFkYXRhICE9PSBudWxsIHx8IHR5cGVvZiBvcHRzLm1ldGFkYXRhICE9PSAndW5kZWZpbmVkJyl7XG5cdFx0b3B0cy5tZXRhZGF0YSA9IG9wdHMubWV0YWRhdGEgfHwgb3B0cy5iYXNlX21ldGFkYXRhXG5cdH07XG5cdG9wdHMuY29udGFpbmVyID0gY2hhcnRcblx0ZmxvdXJpc2hfdmlzdWFsaXNhdGlvbiA9IG5ldyBmbG91cmlzaGxpdmVBcGkuTGl2ZShvcHRzKTtcblx0aWYgKG9wdHMuYmFzZV92aXN1YWxpc2F0aW9uX2lkICYmICFmbG91cmlzaF92aXN1YWxpc2F0aW9uLnRlbXBsYXRlX2xvYWRlZCl7XG5cdCAgZmxvdXJpc2hfdmlzdWFsaXNhdGlvbi50ZW1wbGF0ZV9sb2FkZWQgPSB0cnVlXG5cdH1cbn1cbmV4cG9ydCBkZWZhdWx0ICgpID0+ICh7IHJlbmRlciB9KTtcbiJdLAogICJtYXBwaW5ncyI6ICJBQUdBLE9BQU9BLE1BQXFCLDZEQVE1QixTQUFTQyxFQUFPLENBQUUsTUFBQUMsRUFBTyxHQUFBQyxDQUFHLEVBQStCLENBRTFELElBQUlDLEVBQVEsU0FBUyxjQUFjLEtBQUssRUFDeENBLEVBQU0sR0FBSyxRQUNYRCxFQUFHLFlBQVlDLENBQUssRUFDcEIsSUFBSUMsRUFBT0gsRUFBTSxJQUFJLGFBQWEsRUFDOUJHLEVBQUssd0JBRVJBLEVBQUssc0JBQXdCLE9BQU9BLEVBQUsscUJBQXFCLEVBQzlEQSxFQUFLLFNBQVdBLEVBQUssY0FDckJBLEVBQUssS0FBT0EsRUFBSyxVQUNqQkEsRUFBSyxTQUFXQSxFQUFLLGNBRXJCQSxFQUFLLE1BQVEsQ0FBRSxHQUFHQSxFQUFLLFdBQVksR0FBR0EsRUFBSyxLQUFNLEdBRTVDQSxFQUFLLHVCQUF5QkEsRUFBSyxPQUFTLE9BQ2pEQSxFQUFLLEtBQU9BLEVBQUssS0FDakJBLEVBQUssU0FBV0EsRUFBSyxXQUVqQkEsRUFBSyxXQUFhLE1BQVEsT0FBT0EsRUFBSyxTQUFhLE9BQ3ZEQSxFQUFLLFNBQVdBLEVBQUssVUFBWUEsRUFBSyxlQUV2Q0EsRUFBSyxVQUFZRCxFQUNqQix1QkFBeUIsSUFBSUosRUFBZ0IsS0FBS0ssQ0FBSSxFQUNsREEsRUFBSyx1QkFBeUIsQ0FBQyx1QkFBdUIsa0JBQ3hELHVCQUF1QixnQkFBa0IsR0FFNUMsQ0FDQSxJQUFPQyxFQUFRLEtBQU8sQ0FBRSxPQUFBTCxDQUFPIiwKICAibmFtZXMiOiBbImZsb3VyaXNobGl2ZUFwaSIsICJyZW5kZXIiLCAibW9kZWwiLCAiZWwiLCAiY2hhcnQiLCAib3B0cyIsICJ3aWRnZXRfZGVmYXVsdCJdCn0K
