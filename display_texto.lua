function initialize(box)
  dofile(box:get_config("${Path_Data}") .. "/plugins/stimulation/lua-stimulator-stim-codes.lua")
  state = 0
  state_start_time = 0
end

function process(box)
  local t = box:get_current_time()

  -- Estado 0: inicio → envía imagen 1
  if state == 0 then
    box:send_stimulation(1, OVTK_StimulationId_Label_00, t, 0)
    state_start_time = t
    state = 1

    -- Estado 1: espera 5 seg con imagen 1
  elseif state == 1 then
    if t >= state_start_time + 5 then
      -- Envía imagen 2
      box:send_stimulation(1, OVTK_StimulationId_Label_02, t, 0)
      state_start_time = t
      state = 2
    end

    -- Estado 2: espera 10 seg con imagen 2
  elseif state == 2 then
    if t >= state_start_time + 10 then
      -- Cierra pantalla
      box:send_stimulation(1, OVTK_StimulationId_VisualStimulationStop, t, 0)
      state = 3
    end

    -- Estado 3: terminado, no hacer nada
  end
end

function uninitialize(box)
end
