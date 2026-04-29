function initialize(box)
  dofile(box:get_config("${Path_Data}") .. "/plugins/stimulation/lua-stimulator-stim-codes.lua")
end

function process(box)
  local t

  -- Imagen 1: fondo negro aparece
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_Label_00, t, 0)

  -- Espera 3 segundos
  while box:get_current_time() < t + 60 do
    box:sleep()
  end

  -- Imagen 2: texto aparece
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_Label_02, t, 0)

  -- Espera 3 segundos
  while box:get_current_time() < t + 180 do
    box:sleep()
  end

  -- Detiene el escenario
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_Label_03, t, 0)
end

function uninitialize(box)
end
