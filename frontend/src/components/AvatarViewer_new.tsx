import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { FBXLoader } from "three/examples/jsm/loaders/FBXLoader.js";

interface AvatarViewerProps {
  currentAnimation?: string;
  onAnimationChange?: (animation: string) => void;
}

export default function AvatarViewer({ currentAnimation = "Breathing Idle", onAnimationChange }: AvatarViewerProps): JSX.Element {
  const mountRef = useRef<HTMLDivElement | null>(null);
  const [loadedAnimations, setLoadedAnimations] = useState<{ [key: string]: THREE.AnimationAction }>({});
  const [currentAction, setCurrentAction] = useState<THREE.AnimationAction | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!mountRef.current) return;

    // Scene + renderer
    const scene = new THREE.Scene();
    scene.background = null;

    const width = mountRef.current.clientWidth || 200;
    const height = mountRef.current.clientHeight || 300;

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(width, height);
    renderer.outputEncoding = THREE.sRGBEncoding;

    mountRef.current.appendChild(renderer.domElement);

    // Lighting
    const ambient = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambient);
    const dir = new THREE.DirectionalLight(0xffffff, 5);
    dir.position.set(5, 10, 7.5);
    scene.add(dir);

    const loader = new FBXLoader();
    const clock = new THREE.Clock();
    let mixer: THREE.AnimationMixer | null = null;
    let avatarRoot: THREE.Group | null = null;
    let animationActions: { [key: string]: THREE.AnimationAction } = {};

    function frameObject(object: THREE.Object3D) {
      const box = new THREE.Box3().setFromObject(object);
      const size = box.getSize(new THREE.Vector3());
      const center = box.getCenter(new THREE.Vector3());

      object.position.x -= center.x;
      object.position.z -= center.z;
      object.position.y -= box.min.y;

      const maxDim = Math.max(size.x, size.y, size.z);
      const fov = (camera.fov * Math.PI) / 180;
      let cameraZ = Math.abs((maxDim / 2) / Math.tan(fov / 2));
      cameraZ *= 1.5;
      camera.position.set(0, size.y * 0.55, cameraZ);
      camera.lookAt(0, size.y * 0.55, 0);
    }

    // Function to switch animations smoothly
    function switchAnimation(newAnimationName: string) {
      if (!animationActions[newAnimationName]) {
        console.warn(`⚠️ Animation "${newAnimationName}" not found`);
        return;
      }

      const newAction = animationActions[newAnimationName];
      
      if (currentAction && currentAction !== newAction) {
        // Fade out current animation
        currentAction.fadeOut(0.3);
      }

      // Fade in new animation
      newAction.reset().fadeIn(0.3).play();
      setCurrentAction(newAction);
      
      console.log(`🎭 Switched to animation: ${newAnimationName}`);
      
      if (onAnimationChange) {
        onAnimationChange(newAnimationName);
      }
    }

    // Load main avatar
    loader.load(
      "/Animations/my_avatar.fbx",
      (avatarModel: THREE.Group) => {
        console.log("✅ Avatar model loaded");

        avatarRoot = avatarModel;
        
        // Scale and position avatar
        const desiredHeight = 1.6;
        const box = new THREE.Box3().setFromObject(avatarModel);
        const size = box.getSize(new THREE.Vector3());
        if (size.y > 0) {
          const scaleFactor = desiredHeight / size.y;
          avatarModel.scale.setScalar(scaleFactor);
        }
        
        scene.add(avatarModel);
        frameObject(avatarModel);

        // Set up animation mixer
        mixer = new THREE.AnimationMixer(avatarModel);

        // Load all animation files
        const animationFiles = [
          { name: "Breathing Idle", file: "/Animations/Breathing Idle.fbx" },
          { name: "Waving (1)", file: "/Animations/Waving (1).fbx" },
          { name: "Talking (1)", file: "/Animations/Talking (1).fbx" },
          { name: "Dancing", file: "/Animations/Dancing.fbx" },
          { name: "Backflip", file: "/Animations/Backflip.fbx" }
        ];

        let loadedCount = 0;
        const totalAnimations = animationFiles.length;

        animationFiles.forEach(({ name, file }) => {
          loader.load(
            file,
            (animationModel: THREE.Group) => {
              if (animationModel.animations && animationModel.animations.length > 0) {
                const clip = animationModel.animations[0];
                const action = mixer!.clipAction(clip);
                action.setLoop(THREE.LoopRepeat, Infinity);
                animationActions[name] = action;
                
                console.log(`✅ Animation loaded: ${name}`);
                
                loadedCount++;
                if (loadedCount === totalAnimations) {
                  // All animations loaded, start with breathing idle
                  setLoadedAnimations({ ...animationActions });
                  switchAnimation("Breathing Idle");
                  setIsReady(true);
                  console.log("🎬 All animations loaded and ready!");
                }
              }
            },
            undefined,
            (error: any) => {
              console.error(`❌ Failed to load animation ${name}:`, error);
              loadedCount++;
              if (loadedCount === totalAnimations) {
                setLoadedAnimations({ ...animationActions });
                if (Object.keys(animationActions).length > 0) {
                  const firstAnimation = Object.keys(animationActions)[0];
                  switchAnimation(firstAnimation);
                  setIsReady(true);
                }
              }
            }
          );
        });
      },
      undefined,
      (error: any) => {
        console.error("❌ Failed to load avatar model:", error);
      }
    );

    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      
      if (mixer) {
        mixer.update(clock.getDelta());
      } else if (avatarRoot) {
        // Fallback breathing animation when mixer isn't ready
        const t = clock.elapsedTime;
        avatarRoot.position.y = Math.sin(t * 1.5) * 0.01;
      }
      
      renderer.render(scene, camera);
    }

    animate();

    // Handle resize
    function handleResize() {
      if (!mountRef.current) return;
      const newWidth = mountRef.current.clientWidth || 200;
      const newHeight = mountRef.current.clientHeight || 300;
      
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    }

    window.addEventListener('resize', handleResize);

    // Expose animation switching function globally for Ayora integration
    (window as any).switchAvatarAnimation = switchAnimation;

    return () => {
      window.removeEventListener('resize', handleResize);
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      scene.clear();
      renderer.dispose();
      (window as any).switchAvatarAnimation = undefined;
    };
  }, [onAnimationChange]);

  // React to currentAnimation prop changes (from Ayora)
  useEffect(() => {
    if (currentAnimation && loadedAnimations[currentAnimation] && (window as any).switchAvatarAnimation) {
      (window as any).switchAvatarAnimation(currentAnimation);
    }
  }, [currentAnimation, loadedAnimations]);

  return (
    <div 
      ref={mountRef} 
      className="fixed bottom-0 right-4 w-50 h-75 z-40 pointer-events-none"
      style={{ 
        width: '200px',
        height: '300px',
        background: 'transparent',
        filter: 'drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1))'
      }}
    >
      {/* Loading indicator */}
      {!isReady && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white/80 rounded-lg p-2">
          <div className="text-sm text-gray-600">Loading Ayora...</div>
        </div>
      )}
      
      {/* Animation status indicator (development only) */}
      {process.env.NODE_ENV === 'development' && isReady && (
        <div className="absolute top-2 left-2 bg-black/70 text-white px-2 py-1 rounded text-xs">
          🎭 {currentAnimation}
        </div>
      )}
    </div>
  );
}
