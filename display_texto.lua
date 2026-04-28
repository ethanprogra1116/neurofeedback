function initialize(box)
  dofile(box:get_config("${Path_Data}") .. "/plugins/stimulation/lua-stimulator-stim-codes.lua")
  done = false
end

function process(box)
  -- Para que termine automaticamente y que cuando se cierre el box no se siga ejecutando
  if done then return end
  done = true

  local t

  -- Imagen 1: fondo negro aparece
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_Label_00, t, 0)

  -- Espera 5 segundos
  while box:get_current_time() < t + 5 do
    box:sleep()
  end

  -- Imagen 2: texto aparece
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_Label_02, t, 0)

  -- Espera 10 segundos
  while box:get_current_time() < t + 10 do
    box:sleep()
  end

  -- Cierra pantalla
  t = box:get_current_time()
  box:send_stimulation(1, OVTK_StimulationId_VisualStimulationStop, t, 0)
end

function uninitialize(box)
end
