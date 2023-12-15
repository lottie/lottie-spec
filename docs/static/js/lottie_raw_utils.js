class LottiePlayer
{
    constructor(container, lottie, auto_load=true, custom_options={})
    {
        if ( typeof container == "string" )
            this.container = document.getElementById(container);
        else
            this.container = container;

        this.lottie = lottie;

        this.anim = null;

        this.load_ok = true;
        this.autoplay = true;

        this.custom_options = custom_options;

        if ( auto_load )
            this.reload();
    }

    reload(extra_options={})
    {
        var options = {
            container: this.container,
            renderer: 'svg',
            loop: true,
            autoplay: this.autoplay,
            ...this.custom_options,
            ...extra_options,
        };

        this.on_reload();

        if ( !this.lottie )
            return;
        else if ( typeof this.lottie == "string" )
            options.path = this.lottie;
        else
            options.animationData = lottie_clone(this.lottie);

        let frame;

        if ( this.anim != null )
        {
            frame = this.anim.currentFrame;
            this.clear();
        }

        if ( this.load_ok )
        {
            this.anim = bodymovin.loadAnimation(options);
            if ( frame != undefined )
                this.go_to_frame(frame);
        }
    }

    play()
    {
        this.anim.play();
        this.autoplay = true;
    }

    pause()
    {
        this.anim.pause();
        this.autoplay = false;
    }

    on_reload()
    {
    }

    clear()
    {
        try {
            if ( this.anim )
            {
                this.anim.destroy();
                this.anim = null;
            }
        } catch ( e ) {}
    }

    go_to_frame(frame)
    {
        if ( this.autoplay )
            this.anim.goToAndPlay(frame, true);
        else
            this.anim.goToAndStop(frame, true);
    }
}
