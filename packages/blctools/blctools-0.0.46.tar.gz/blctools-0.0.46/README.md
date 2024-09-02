# BLC Data Analytics tools package

Data Analytics helper functions to work with inside BLC's Cloud system.

# Changelog

## Version 0.0.46

* **cl_PPO()**:
    - When descargar=True, it downloads only missing files now.

* **cl_DTE()**:
    - When descargar=True, it downloads only missing files now. 

* **dirs.extraer()**:
    - added parameter "eliminar". If true, deletes  zip files after succesful extraction.

* **cl_ApiCammesa()**:
    - Solved bug when trying to download reports between dates with no actual data.

* **cl_ReporteBase()**:
    - Added parameter "eliminar" to .descargar() method (see, dirs.extraer() updates)

* **cl_TablasVC()**:
    - Included "central_contratos" and "contratos" to the downloaded data and modified all corresponding functions.
    - Included "respaldar_datos_basicos" and "respaldar_incidencias" to let the user choose wheter or not to backup queried data.
    - Changed .__asignar_datos_smec_() method, to assign "nemoCammesa" and "unidadComercial" from the "central_contratos" table.
    - Added .__asignar_datos_central_contratos().
    - Added .__asignar_datos_contratos().

* **cl_SQLConnector()**:
    - Now compatible with sqlalchemy >= 2

## Version 0.0.45
    - No log (lost)

## Version 0.0.44

* **dirs**
    - Corrected bug when extracting zip files
* **cl_SQLConnector()**
    - Made compatible with SQLAlchemy => 2.0

* **DatosCROM()**
    - Improved: elaborar_curvas_de_potencia can now accept other dataframes.

## Version 0.0.43
* **DatosSMEC()**
    - Improved: estimar_ENS_xxxx now runs orders between 10x (metodo='cuantil') and 40x (metodo='promedio') faster. Now they both run equally fast.

## Version 0.0.42
* **DatosSMEC()**
    - Fixed bug: Initialization was not working properly.

## Version 0.0.41
* **DatosCROM()**
    - Improved: all functions to estimate ENS were improved drastically. They're now 4x faster.

## Version 0.0.40
* **DatosCROM()**
    - Fixed bug: buscar_indisponibilidades() was not working properly
    - Fixed bug: buscar_limitaciones() was not working properly
    - Fixed bug: buscar_incidencias() was not working properly

## Version 0.0.39
* **DatosCROM()**
    - Fixed bug: consolidar_todo() was not categorizing internal/external incidents correctly for some reason

## Version 0.0.38
* **DatosCROM()**
    - Fixed bug: exportar() really slow
    - Improved: explotar_incidencias() takes  only incidencts with different start and end dates as input
    - Improved: Some functions were being executed twice upon object initialization

## Version 0.0.37
* **fechas**
    - Fixed bug: mes_ant_dia_1() wasn't working properly.

## Version 0.0.36
* **DatosCROM()**
    - Fixed bug: incidencias_resumen_status wasn't working properly

* **TablasVC()**
    - Fixed bug: Functions .consultar_.... where not working with "uc" parameter

## Version 0.0.35
* **DatosCROM()**
    - Added: incidencias_resumen_status attribute
    - Deleted: Client attribute
    - Changed: resumen_diario_incidencias to incidencias_resumen_diario

* **TablasVC()**
    - Deleted: Client attribute
  
* **PPO()**
    - Changed: Default dates on initialization are now blctools.ayer()

* **DTE()**
    - Changed: Default dates on initialization are now blctools.ayer()
    - Changed: Improved internal modilarity
    - Changed: "dolarizar" parameter to "cols_usd"
    - Added: "dolarizar" method

## Version 0.0.34
* **BCRA()**
    - Fixed bug: rem 24 month projections were not being projected properly

## Version 0.0.33
* **BCRA()**
    - Added: cargar_tc_min = False as initialization parameter
    - Added: tc_min as the retail price for the USD in ARS
    - Fixed bug: rem projections were not being projected properly

## Version 0.0.32
* **fechas**
    - Fixed bug: restar_mes wasn't working for some months of the year.

## Version 0.0.31
* **ArchivoMDB()**
    - New object: It serves as an easy way to explore .mdb files

* **ReporteBase()**
    - Changed: how the object processes mdb files. It's now more efficient

## Version 0.0.30
* **BCRA()**
    - Changed: On initializing, rem tryies to download all files
    - Changed: nor .rem_tc table is called .tc_rem
    - Changed: now obtener_rem_mensual() is called cargar_rem()
    - All possible attributes are nor .tc_dia, .tc_udh, .tc_rem and .rem

* **DTE()**
    - Changed: Cargar DTE goes on even if tc_udh couldn't be loaded from BCRA() object

* **DatosSMEC()**
    - Changed: consultar_datos_vc() is now cargar_datos_vc()

## Version 0.0.29
* **DTE()**
    - Added: Option to convet prices to USD
    - Added: Initialization parameters cargar (bool), descargar (bool) and dolarizar (str,list,tuple,set)

* **.fechas**
    - Added: lista_mensual. Returns a list of dates provided a starting date and an "n"
    - Added: convertir_año_a_fecha() Returns a dt.DateTime object, starting from an integer (year)
    - Fixed bug: mes_ult_dia wasn't allowing for future dates

* **BCRA()**
    - Added: Added interface with Argentina's Central Bank to download exchange rate (tc) and Market Expectations (REM)

* **DatosCROM()**
    - Fixed bug: After 0.0.25 update, the object wasn't reading .xlsx files properly, thus crashing when trying to read.

## Version 0.0.28
* **DatosSMEC()**
    - Changed: FechaOp column is now datetime type, when Querying VisionCROM's database.

## Version 0.0.27
* **DatosSMEC()**
    - Fixed bug: HoraOp on cargar_datos_prn was not being calculated correctly.  
    - Fixed bug: Actaris meters have now the right column order.
    - Changed: Now E_Neta_Gen and E_Neta_Con are calculated when each file is read, for consistency.

## Version 0.0.26

* **DatosCROM()**
    - Added .DatosCROM() now warns if there is an empty excel file

* **DatosCdO()**
    - Added strings report
    - Changed the variable-reading process, made it more efficient. By adding .pickle file as backup.
    - Added listado_señales_strings(): get list of "string" signals (actually DC combiner boxes)
    - Added descargar_datos_strings(): download "string" signals' mesaurements (actually DC combiner boxes)

* **DatosSMEC()**
    - Added this new object to interact with VisionCROM's DataBase and fetch SMEC measurements 
      - Initialization parameters:
        - fecha_i = Data's start date. DateTime object with year, month, day, hour and minute interval.
        - fecha_f = Data's end date. Same as fecha_i
        - parques = CAMMESAS's Nemotécnicos to indicate from which park the measurements will be retrieved
        - dir_salida = export directory
        - cargar_datos_basicos = sames as TablasVC()
        - mensajes = Verbose while loading
        - mensajes_SQL = Verbose while connecting
    - Added consultar_datos_vc(): Query VisionCROM's database using fecha_i, fecha_f and parque attributes
    - Added leer_archivo_prn(file): Read a single .prn file
    - Added cargar_datos_prn(folder): Read every .prn file in a given folder

## Version 0.0.25
* **TablasVC()**
    - Changed: modificar_incidencia() now doesn't affect .incidencias_todas_auditoria attribute.

* **DatosCROM()**
    - Improved: .estimar_ENS_varias_incidencias()'s overall speed and precision. Still not good for production, but better for single WTG incidents. 
    - Improved: Memory Usage overall
    - Removed : Pgen_U variable, was a duplicate of FC.
    - Removed: Pcon_U, Egen_U, Econ_U, Epos_U, very rarely useed, could be calculated by hand.

* **DatosCdO()**
    - Added this new object to interact with InAccess' API and download raw data from Caldenes del Oeste solar PV Plant (CdO)
      - Initialization parameters:
        - usr = Username (SCADA's username)
        - pwd = PAssword (SCADA's password)
        - apikey = Private apikey provided from InAccess
        - fecha_i = Data's start date. DateTime object with year, month, day, hour and 10 minute interval.
        - fecha_f = Data's end date. Same as fecha_i
        - reporte_produccion = True / False. Indicate if production report should be downloaded automatically
        - reporte_trackers = True / False. Indicate if trackers report should be downloaded automatically
        - reporte_mensual = True / False. If True, downloads both reports. False has no effect.
        - exportar = True / 'todos' / 'produccion / 'trackers'. 
          - If True or 'todos' exports everything. 
          - 'produccion' and 'trackers' export the respective report each.
    - Added obtener_señales(): Takes in a dataframe of Measurement Locations (Mlocs) and fetches all possible signals.
    - Added obtener_mediciones(): Takes a dataframe of signal lists and fetches data
    - Added listado_señales_trackers(): Just a preset, that shows which signals are used for the monthly production report
    - Added listado_señales_produccion(): Just a preset, that shows which signals are used for the monthly tracker report
    - Added mediciones_disponibles(): Initializing function that loads every available signal, from BLC's cloud
    - Added descargar_datos_produccion(): Downloads data from listado_señales_produccion() signals using DatosCdO's start and end date parameters
    - Added descargar_datos_trackers(): Downloads data from listado_señales_trackers() signals using DatosCdO's start and end date parameters
    - Added exportar(reportes = str): Exports loaded data from preset reports ['todos', 'produccion', 'trackers'].
  
## Version 0.0.24

* **DatosCROM()**
    - estimar_ENS() now subtracts actual generated power from estimated power loss
    - Fixed bug: estimar_ENS() wasn't checking datatypes properly

## Version 0.0.23
* **PPO() and DTE()**
    - Fixed bug: Setting "filtro" on initialization had no effect on running functions with default parameters.

* **cl_CarpetaServicios()**
    - Added: blctools now finds "Servicios" folder, even when it's not explicitly written in the OS Path.

* **DatosCROM()**
    - Added: estimar_ENS() takes a list of ids and estimates the ENS for each incident, based on actual production values.
    - Added: estimar_ENS_incidencias_abiertas() fills the ENS of the incidents that are still open
    - Added: estimar_ens_inc_abiertas = False initialization parameter
    - Added: incidencias_a_editar = None, takes a dictionary of dictionaries. The first dict has the IDs of the incidents that have to be edited as keys and their corresponding values are a second dictionary that holds the new parameters (and new values) . Example: {18088:{ENS=800,Owner='NewOwner'},18089:{Hours=8,Origin='INT'}}
    - Fixed bug: Plant Active Power and Energy was being calculated from WTGs / Circuits and it shouldn't. It has it's own values
    - Excludes incidents with Hours or ENS < 0 on .incidencias and .incidencias_redux attributes, but not in incidencias_todas
    - cargar_incidencias is now False as default.
    - explotar_incidencias is now False as default.

* **Fechas module**
    - Fixed bug: hora_op, fecha_op, sumar_mes / restar_mes now have prevenir_futuro=False as default parameter and pass it to validar_fecha(s)
    - Fixed bug: obtener_periodo now has prevenir_futuro=True as default parameter and passes it to mes_periodo(s)
  
* **TablasVC()**
    - Added .consultar_agrupamiento_de_un_equipo() 
    - Added .modificar_incidencia() to edit a current incident
    - Fixed Bug: Query for incidencias was not returning open incidents

## Version 0.0.22
* **DatosCROM()**
    - Added: One can now initialize the "parques" parameter with a single string, to avoid using brackets when working with just one park.
    - Fixed bug: Eerror when no active incidents were found for a given parq/period and trying to .interpretar_incidencias_bajo_iec61400()
    - Fixed bug: Some functions where trying to call TablasVC().consultar_incidencias() which doesn't exist anymore. Now its .consultar(incidencias='offline')

## Version 0.0.21
* **DatosCROM()**
    - Added: .buscar_indisponibilidades(). Searches for periods of time which the WTGs met certain condition filters of out of service
    - Added: .buscar_limitaciones(). Searches for periods of time which the PLANT or WTGs had an SP_P > than the max.
    - Added: .buscar_incidencias() combines both previous functions in a single line. 
    - Added: .incidencias_autodetectadas attribute, with export capabilities
    - Added: "Status" column to incidencias_redux
    - Added: "Count" and "Histogram" columns when calculating powercurves. _count "sheet" on export is now always there.
    - Added: "explotar_incidencias" initialization parámeter, which can take either 'iec61400' (default) or 'crudas'
    - Fixed bug: Missing Indices on datos_seg when trying to consolidate incidents and 10second data
    - _identificar_indisponibilidades() pgen and ppos parameters were added, to further improve filtering capacity
    - __procesar_d10s_dc() and cargar_segundales() now use DataFrame.reindex() to fill with blank rows where necessary.
    - elaborar_curvas_de_potencia() now sorts index clockwise instead of alphabetically

* **TablasVC()**
    - Added .consultar_agrupamiento_de_un_equipo() 

## Version 0.0.20
* **DatosCROM()**
    - interpretar_incidencias_bajo_iec61400() made more efficient, while keeping compatibility with pandas >= 1.5.0
    - _identificar_indisponibilidades() pgen and ppos parameters were added, to further improve filtering capacity
* **TablasVC()**
    - Added "potencia=False" parameter to consultar_agrupamientos(), consultar_equipos_no_agrupamientos() 

## Version 0.0.19
* **DatosCROM()**
    - Fixed bug: interpretar_incidencias_bajo_iec61400() was experiencing problems with pandas >= 1.5.0, and had a problem with the index selection statement at the beginning.
    - Added experimentally: _identificar_indisponibilidades(duracion=30)

## Version 0.0.18
* **DatosCROM()**
    - .exportar() now flattens MultiIndex columns, freezes panes and formats floats, for easier view on Excel.
    - Added "invalidar_datos_seg_congelados" initialization parameter (default = False)
    - Fixed bug: .exportar() throwing error when curvas_de_potencia or consolidado held more than 1 Dataframe
    - Fixed bug: .interpretar_incidencias_bajo_iec61400() now trims final result between fecha_i and fecha_f
    - Fixed bug: .elaborar_curvas_de_potencia() wasn't working properly with filtro_n >1

## Version 0.0.17
* **fechas submodule**
    - Added .sem_dia_1(date,offset=0) function. Returns first day of week of the given date + given offset in days (offset can be negative)
    - Added .sem_act_dia_1(offset=0) function. Returns first day of current week + given offset in days
    - Added .año_op(fecha_actual,fecha_cod) function. Returns the current contractual year based on the two dates (First year is 1, not 0)
* **DatosCROM()**
    - adjusted how xlsx files processing time is calculated
    - adjusted how .pickle files are created/read. Compression was added through bz2
    - consolidado attribute is now called consolidado_redux, which is a subset of columns of consolidado
    - consolidado attribute now holds all the original data, but resampled to the users' input sample rate, excluding categorical variables
    - consultar_equipos_parque() and consultar_equipos_parque_no_agrupamientos() are now called consultar_equipos() and consultar_equipos_no_agrupamientos()
    - __iec61400_preparar_df_vacio_minutal() and it's aux methods are now more efficient
    - Added variables "Gen", "Con", "Pos" as boolean series for each equipment, into the datos_seg dataframe
    - Added columns "ENS_Lim","ENS_LimExt","ENS_LimInt","ENS_Ind","ENS_IndExt,"ENS_IndInt" to "consolidado" report
    - Added variable "Datos_%" which indicates the ammount of not null data per row, per element, into the datos_seg dataframe
    - Added variable "Registros" which indicates the ammout of rows (measured in time) on the excel file for that given element. Should alwasy equal 24
    - Fixed bug: .__procesar_d10s_5i() wasn't ensuring boolean dtypes for 'Gen','Con' and 'Pos', which impacted negatively on .elaborar_reporte_consolidado()
    - Fixed bug: .consolidar_todo() wasn't working with PEGARCIG 
    - Fixed bug: .consolidar_todo() wasn't working adding up HOUR columns properly (the rest was fine)
    - Fixed bug: .consolidar_todo() wasn't finishing if there weren't any incidents for a given park on a given time window
    - Fixed bug: .explotar_incidencias() now works properly if there aren't any incidents on a given time window
    - Fixed bug: .exportar() was exporting empty dataframes, since they were not "None"
    - Fixed bug: Roll-up of availability parameters wasn't being done correctly. Now groupings are the mean or logic operator of their groupped elements.    
    - Fixed bug: 10s pre-processing: Wind_dir_r was not being saved correctly for 'PLANT' element on self.datos_seg
    - Fixed bug: 10 second data is now being completed (in case of missing 10second records) with null values. This could have lead to serious problems when 
    - Fixed bug: On many methods. From pandas >= 1.5.0 numpy series where linked and not copied when creating a new df. This created many bugs throughout the whole program. 
    - unloading incidents to the 10 second data, since the main mechanism behind it is selection trhough .loc[t_stamp,:] 
* **TablasVC()**
    - Added attributes .habilitaciones and .tipohabilitaciones which are new tables of "datos básicos". They contain COD related information of each plant
    - Added .consultar_cod(nemo_parque='',uc='') function, to quickly find out about a plant's COD (Birthday) date (grabs from the table above)
    - Added .consultar_año_op(fecha_actual,feca_cod) function. Returns the contractual year (Contractual age) of a power plant
    - Added .__crear_dict_tipo_empresa(). Which fills in thre internal attributes: _empresas_bop, _empresas_gen, _empresas_grid
    - Fixed bug: .consultar() would fetchdatos_basicos from offline file even when 'online' parameter was set. This was due to:
      -  a logic error of variable db_off inside .consultar()
      -  the order in which instructions were executed
    - Fixed bug: __procesar_incidencias_it2() wasn't executing properly when cargar_datos_basicos = 'offline' was set. Solved by calling the new function .__crear_dict_tipo_empresa() before business mapping
    - Fixed bug: Desconecting twice from DB when fetching incidencias
    - Fixed bug: __combinar_incidencias_locales_y_online() wasn't working properly. Duplicate dropping should only be done by 'ID'
    - Refactored __asignar_datos() .method, to make it modular per table

## Version 0.0.16
* **DatosCROM()**
    - Added data invalidation when processing 10 second data. Now consecutive values of P, Q, Wind, Wind_dir and PPos != 0 and != max (for Ppos) are replaced with np.nan
    - Fixed bug when selecting no .parques ( [] ) and initializing a DatosCROM object
    - Fixed bug when truying to export specific reports through the generating functions (ie elaborar_curvas_de_potencia, interpretar_bajo_iec61400, etc.) and seeting the "exportar" parameter to True
    - Fixed bug. PI wasn't being correctly calculated. (* instead of / was being used)
    - Added "filtro_n" parameter to .elaborar_curvas_de_potencia(), to only show results with an n_count >= n per bin. Default 0 (deactivated)
    - Added feature. Ppos is being calculated if column doesn't exist, based on Curvas_de_potencia.xlsx on BLC's cloud under blc.get_dc_cfg() directory
    - "clientes" initializing parameter was removed (little use for it)
    - "solo_CROM" initializing parameter was removed (little use for it)
* **TablasVC()**
    - Improved the processing of incidents, now "Origin" is "NA" and np.nan resistent. Default = "INT"
    - Fixed bug through which a filter for discarded incidents wasn't working.
    - Refactored processing of incidents, it's more readable now

## Version 0.0.15
* **DatosCROM()**
    - .exportar() was added. Helper function to export all loaded reports to xlsx format.
    - .explotar_incidencias() now takes in optional export parameters.
    - .incidencias_interpretar_bajo_iec61400() now takes in optional export parameters.
    - .incidencias_identificar_solapamientos() was added.
    - "curvas_de_potencia" parameter added while initializing, to force power curves to be computed automatically
    - .elaborar_curvas_de_potencia() is now more resistent to failures. Powercurves can be elaborated without having to process incidents before, although not recommended if user doesn't know what he is doing.
    - changed how __renombrar_lvl0() works, now it must be feed the equipment names.
* **TablasVC()**
    - fixed a bug, where .consultar_equipos_parque_no_agrupamientos would return "PLANT" twice for GRIOEO
    - "cargar_incidencias" and "cargar_datos_basicos" parameters added while initializing, with possible values being [Flase, True, 'offline', 'online']
    - now queries per default active incidents from the 1st day of two months prior to today (if True or 'online' values where passed to "cargar_incidencias" parameter). Then concatenates obtained results with offline results (if there are any).

## Version 0.0.14
* **TablasVC()**
    - Fixed bug: Corrected functions that took equipments from blctools.TablasVC().conjuntogeneradores, now reading from .tipoequipo
    - Fixed bug: Now Parks without any grouping of it's generators can return the generators without grouping. Special Case: PEGARCIG
* **SQLConnector()**
    - now decrypts login data from BLC's secure fileserver.
* **DatosCROM()**
    - .consultar_equipos_parque() now retrieves the right elements if the plant doesn't havy any other grouping stages
    - .consultar_equipos_por_agrupamiento() now returns an empty list if the plant doesn't havy any other grouping stages
    - .rpt_consolidado(granularidad='1D') was added.
    -  "forzar_reprocesamiento" parameter added while initializing, to force re-process 10 second data.
    - .rpt_curvas_de_potencia() was added
    - changed the behaviour of .fecha_i and .fecha_i setters. They now attempt to update "incidencias" and "archivos" depending on the values of fecha_i and fecha_f, but the setters dont try to order the dates automatically, which lead to an unwanted behaviour.
    - Changed completely how DatosCROM() now proceses raw data (10 seconds and Incidencias). It's more efficient, and the heavy lifting occurs while processing the 10-second data. Now index has 1 column (Time) and columns have a 3 level structure (p,e,v) = Park, Element, Variable

## Version 0.0.13
* Created SQLConnector class to migrate to SQLAlchemy
* blctools.TablasVC now inherits from SQLConnector

## Version 0.0.12
* Function blctools.fechas.obtener_periodo() was added (moved from blctools.ReporteBase())
* Added more parameter flexibility within all functions inside blctools.fechas.
* Objects PPO(), DTE() and DatosCROM() now accept the "periodo" initialization parameter (overrides fecha_i and fecha_f).
* bjects blctools.DatosCROM() and blctools.TablasVC() have now the "solo_CROM=False" initialization parameter.
* function blctools.TablasVC.consultar_nemoCammesa() has now the "solo_CROM=False" argument  

## Version 0.0.11
* Corrected blctools.PPO.periodo('mes_anterior')
* Function ReporteBase.a_excel() accepts now the parameter "exportar_consulta=bool"
* Objects PPO() and DTE() now accept the following initialization parameters
    - "filtro"
    - "periodo" (overrides fecha_i and fecha_f)
* No more unnecessary warnings on changing the "filtro" parameter
* Function blctools.fechas.mes_dia_1() and blctools.fechas.mes_ult_dia() now validate dates using blctools.fechas.validar_fechas()
* Functions blctools.fechas.validar_fecha() and .validar_fechas() now have a parameter "prevenir_futuro=True" as default, to prevent future dates or not.
* Fixed a bug, when changing "filtro" on functions of child classes of DTE() or PPO(), download and extraction directories wouldn't update properly.

## Version 0.0.10
* Attribute blctools.DatosCROM.dir_salida sets to which directory the reports go out to (didn't have much impact before)
* Improved automatic Servicios directory search

## Version 0.0.9
* Removed dependencies list
* Ability to download unfiltered PPOs/DTEs without specifying parks/plants list
* Incidents are no longer loaded by default on blctools.DatosCrom() objects

## Version 0.0.8
* Corrected dependencies list

## Version 0.0.6 ~ 0.0.7
* Bug fixes regarding file management
* Ability to customize filters when hitting CAMMESA's API
* PBA calculation according to IEC61400 is still functioning incorrectly

## Version 0.0.5
* Most of the code is Object Oriented now.
* CAMMESA's forecasts have been added.

## Version 0.0.2 ~ 0.0.4
* Fixed the install issues

## Version 0.0.1
* Basic functionality is up and running

## TO DOs
* Corroborar que la cantidad de grupos de columnas en los archivos 10 segundales, coincida con la cantidad de equipos del parque cuyo nombre de archivo enuncia.
* Convertir DatosCROM().parques a "nemos" automáticamente.
* Mejorar los mensajes de procesamiento nivel 0, 1 y 2 en todas las funciones
* Fix Bug: Code could break by passing an '' element into parques initialization parameter