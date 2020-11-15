
## Electricity generation and carbon intensity
df_select_elec = df_full[(df_full['geo']=='National') & (df_full['year']>=2009) & (df_full['sector']=="Electricity generation")]
# Make lists of you data because of course this type of figure has a completley different syntax again
year_dict = df_select_elec['year'].tolist()
gwh_dict = df_select_elec['elec_gen_GWh_output'].tolist()
elec_carb_int_dict = df_select_elec['elec_carb_int_outp'].tolist()
# create df_select_elec
fig_elec_gen_int = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig_elec_gen_int.add_scatter(x=year_dict, y=gwh_dict, name="Electricity generation", mode="lines", line=dict(width=2, color="rgba(214,39,40,1)"), secondary_y=False,)
fig_elec_gen_int.add_scatter(x=year_dict, y=elec_carb_int_dict, name="Carbon intensity", mode="lines", line=dict(width=2, color="black"), secondary_y=True,)



fig_elec_gen_int.update_layout(template="plotly_white",
                                    legend_traceorder="reversed",
                                    title_text="Electricity generation and carbon intensity",
                                    title_font_color="#1F77B4",
                                    title_font_size=18,
                                    title_font_family="Rockwell",
                                    title_x = 0.02,
                                    margin=dict(t=40, r=0, b=0, l=60, pad=0))
fig_elec_gen_int.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
fig_elec_gen_int.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
# Set y-axes titles
fig_elec_gen_int.update_yaxes(title_text="Electricity generation (GWh)<sub> </sub>", secondary_y=False)
fig_elec_gen_int.update_yaxes(title_text="Carbon intensity (kg CO<sub>2</sub>-eq/kWh)", secondary_y=True)