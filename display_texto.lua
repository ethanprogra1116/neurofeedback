function initialize(box) -- initialize tiene que ir con ese nombre exacto en OpenVibe.
  dofile(box:get_config("${Path_Data}") .. "/plugins/stimulation/lua-stimulator-stim-codes.lua")
end

function process(box) -- process tiene que ir con ese nombre exacto en OpenVibe.
  local t

  -- Fase 1: 2 min ojos cerrados
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_Label_00, t, 0)
  while box:get_current_time() < t + 120 do
    box:sleep()
  end

  -- Fase 2: 2 min ojos abiertos
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_Label_01, t, 0)
  while box:get_current_time() < t + 120 do
    box:sleep()
  end

  -- Fase 3: 3 min lectura
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_Label_02, t, 0)
  while box:get_current_time() < t + 180 do
    box:sleep()
  end

  -- Fase 4: 5 min explicación
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_Label_03, t, 0)
  while box:get_current_time() < t + 300 do
    box:sleep()
  end

  -- Detiene el escenario
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_Label_04, t, 0)
end

function uninitialize(box) -- uninitialize tiene que ir con ese nombre exacto en OpenVibe.
end
