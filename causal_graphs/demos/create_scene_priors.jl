#!/usr/bin/env
# # Generate the random variables that will be inputs to the initial scene
# Starting with a occlusion event
# TY 05/13/2020
# add containment
# TY 06/01/2020

# Need to import
#import Pkg
#Pkg.add("General")
#Pkg.add("Gen")
#Pkg.add("JSON")

# Load the necessary things
using Gen
using JSON

# Get the arguments
scene_type=ARGS[1]
trace_number=ARGS[2]
#println(scene_type)
#println(trace_number)

# Define occlusion generative model
@gen function generate_occlusion_scene(x::Int) # how many objects will there be? 
    
    ## 1. Choose the object type 
    # Is it going to be a ball?
    if @trace(bernoulli(0.5), :is_ball)
        
        radius=@trace(uniform(0.005,0.03),:ball_radius)   # 0.02 [m]
        force=@trace(uniform(8,13), :force)
        
    # Or will it be a plank?
    else
        
        plank_l=@trace(uniform(0.01,0.03),:plank_length) # (.02, .025, .02) [m]
        plank_w=@trace(uniform(0.01,0.03),:plank_width)
        plank_h=@trace(uniform(0.01,0.03),:plank_height)
        force=@trace(uniform(0.01,0.04), :force) 
    end
    
    ## 2. Scene-specific things: Occluder
    occl_l=@trace(uniform(0.1,0.4),:occl_length) #(0.1, 0.001, 0.4)  
    occl_w=@trace(uniform(0.0005,0.0001),:occl_width)
    occl_h=@trace(uniform(0.1,0.6),:occl_height) 
    position=@trace(uniform(0,.3), :occl_pos)
      
end;

# Define our generative model
@gen function generate_containment_scene(x::Int) # how many objects will there be?  
    
    ## 1. Choose the object type 
    # Is it going to be a ball?
    if @trace(bernoulli(0.5), :is_ball)
        
        radius=@trace(uniform(0.005,0.03),:ball_radius)   # 0.02 [m]
        #force=@trace(uniform(8,13), :force)
        
    # Or will it be a plank?
    else
        
        plank_l=@trace(uniform(0.01,0.03),:plank_length) # (.02, .025, .02) [m]
        plank_w=@trace(uniform(0.01,0.03),:plank_width)
        plank_h=@trace(uniform(0.01,0.03),:plank_height)
        force=@trace(uniform(-0.002,-0.01), :force) # NEGATIVE here
    end
    
    ## 2. Scene-specific things: Goblet
    goblet_h=@trace(uniform(0.05,0.15),:goblet_h) #(0.1, 0.001, 0.4)  
    goblet_R1=@trace(uniform(0.01,0.06),:goblet_R1)
    goblet_R2=@trace(uniform(0.01,0.06),:goblet_R2) 
    goblet_EPS=@trace(uniform(0.001,0.003), :goblet_EPS)
    
    ## 3. Scene-specific things: Height and angle of ramp
    ramp_h=@trace(uniform(-0.05,0.05),:ramp_h)
    ramp_ang=@trace(uniform(-10,5),:ramp_ang)
      
end;
    
# Function to read the generative trace
function write_gen_trace(trace,scene_type,save_file)
   
    #Is it a ball or a plank? (This is always relevant!)
    is_ball=Gen.get_value(Gen.get_choices(trace),:is_ball)
    
    # Make the dictionary depending on the scene type  
    if scene_type=="occlusion_Gen"
        
        # Get the things just generally relevant to this scene
        force=Gen.get_value(Gen.get_choices(trace),:force)
        occl_l=Gen.get_value(Gen.get_choices(trace),:occl_length)  
        occl_w=Gen.get_value(Gen.get_choices(trace),:occl_width)
        occl_h=Gen.get_value(Gen.get_choices(trace),:occl_height) 
        position=Gen.get_value(Gen.get_choices(trace), :occl_pos)
        
        
        # Then get the relevant information depending on if its a ball or a plank
        # And make the trace that will be saved
        if is_ball
            radius=Gen.get_value(Gen.get_choices(trace),:ball_radius)
            trace_dict = Dict("is_ball" => is_ball,
                "ball_radius" => radius,
                "force" => force,
                "occluder_lwh" => Dict("length" => occl_l, "width" => occl_w, "height" => occl_h),
                "occluder_pos" => position
            )
        else
            plank_length=Gen.get_value(Gen.get_choices(trace),:plank_length)
            plank_width=Gen.get_value(Gen.get_choices(trace),:plank_width)
            plank_height=Gen.get_value(Gen.get_choices(trace),:plank_height)

            trace_dict = Dict("is_ball" => is_ball, 
                "plank_lwh" => Dict("length"=>plank_length,"width"=>plank_width,"height"=>plank_height),
                "force" => force,
                "occluder_lwh" => Dict("length" => occl_l, "width" => occl_w, "height" => occl_h),
                "occluder_pos" => position
            )
        end  
        
    elseif scene_type=="containment_Gen"
    	
    	# Get the things just generally relevant to this scene
        force=Gen.get_value(Gen.get_choices(trace),:force)
        goblet_h=Gen.get_value(Gen.get_choices(trace),:goblet_h)  
        goblet_R1=Gen.get_value(Gen.get_choices(trace),:goblet_R1)
        goblet_R2=Gen.get_value(Gen.get_choices(trace),:goblet_R2) 
        goblet_EPS=Gen.get_value(Gen.get_choices(trace), :goblet_EPS)
        ramp_h=Gen.get_value(Gen.get_choices(trace), :ramp_h)
        ramp_ang=Gen.get_value(Gen.get_choices(trace), :ramp_ang)
        
        # Then get the relevant information depending on if its a ball or a plank
        # And make the trace that will be saved
        if is_ball
            radius=Gen.get_value(Gen.get_choices(trace),:ball_radius)
            
            trace_dict = Dict("is_ball" => is_ball,
                "ball_radius" => radius,
                "force" => force,
                "goblet" => Dict("height" => goblet_h, "R1" => goblet_R1, "R2" => goblet_R2, "EPS" => goblet_EPS),
                "ramp" => Dict("height" => ramp_h, "angle" => ramp_ang)
             )
            
        else
            plank_length=Gen.get_value(Gen.get_choices(trace),:plank_length)
            plank_width=Gen.get_value(Gen.get_choices(trace),:plank_width)
            plank_height=Gen.get_value(Gen.get_choices(trace),:plank_height)

            trace_dict = Dict("is_ball" => is_ball, 
                "plank_lwh" => Dict("length"=>plank_length,"width"=>plank_width,"height"=>plank_height),
                "force" => force,
                "goblet" => Dict("height" => goblet_h, "R1" => goblet_R1, "R2" => goblet_R2, "EPS" => goblet_EPS),
                "ramp" => Dict("height" => ramp_h, "angle" => ramp_ang)
            )
        end  
     
    end
    
    # Put it in a JSON format
    string_dict = JSON.json(trace_dict)
    
    # Save it to the file
    open(save_file, "w") do f
        write(f, string_dict)
    end

    return nothing
end;

# Simulate based on the scene type
if scene_type=="occlusion_Gen"
    
    # Simulate
    trace = Gen.simulate(generate_occlusion_scene, (0,));
    
elseif scene_type=="containment_Gen"
	# Simulate
    trace = Gen.simulate(generate_containment_scene, (0,));
end

# Were you able to define it?
@isdefined(trace) || println(string("ERROR: Gen function not set up for scene type: ",scene_type))

# If so, save!
if @isdefined(trace)
    
    # talk to them 
    println(string("Wrote gen trace to gen_jsons/scene_trace_",scene_type,trace_number,".json"))

    # Write it out
    write_gen_trace(trace,scene_type,string("gen_jsons/scene_trace_",scene_type,trace_number,".json"))

end
