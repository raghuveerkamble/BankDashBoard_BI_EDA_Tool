import React, { Component } from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import '../js/adminlte.js';
import $ from 'jquery';

/**
 * Create a Boostrap 4 dashboard main sidebar.
 */
export default class Sidebar extends Component {
	
	constructor(props) {
        super(props);
	}		

	componentDidMount() {
		this.$el = $(this.el);
		this.$el.Treeview('init');
	}
	
	componentWillUnmount() {
		this.$el.Treeview('destroy');
	}	
	
	render() {
		const {
			children, 
			className,
			disable,
			title,
			skin,
			color,
			brand_color,
			url,
			src,
			elevation,
			opacity,
			loading_state, 
			setProps, 
			...otherProps
		} = this.props;
		
		var BrandTag, ContentTag
		
		if(title!=null) {
			BrandTag = <a 
				className={classnames(
					'brand-link',
					brand_color!=null ? `bg-${brand_color}` : false
				)}
				href={url} 
				target='_blank'
			>
				<img src={src} className="brand-image img-circle elevation-3" style={{opacity: opacity}}></img>
				<span className="brand-text font-weight-light">{title}</span>
			</a>
		}
		
		ContentTag = <div className="sidebar"><nav className = "mt-2">{children}</nav></div>
  
		return(
			<div>
				<aside 
					className={classnames(
						'main-sidebar',
						color!=null ? `sidebar-${skin}-${color}` : `sidebar-${skin}`,
						elevation!=null ? `elevation-${elevation}` : false,
						{hide: disable},
						className
					)}
					ref={el => this.el = el}
					{...otherProps}
					data-dash-is-loading={
						(loading_state && loading_state.is_loading) || undefined
					}
				>
					{BrandTag}
					{ContentTag}
				</aside>
			</div>
		)              
	} 
}
		
Sidebar.defaultProps = { 
	skin: "dark", 
	color: "primary",
	url: '#',
    elevation: 4, 
	opacity: 0.8,
	disable: false
};

Sidebar.propTypes = {
	
	/**
	* The ID of this component, used to identify dash components
	* in callbacks. The ID needs to be unique across all of the
	* components in an app.
	*/
	id: PropTypes.string,

	/**
	* The children of this component.
	*/
	children: PropTypes.node,

	/**
	* Defines CSS styles which will override styles previously set.
	*/
	style: PropTypes.object,

	/**
	* Often used with CSS to style elements with common properties.
	*/
	className: PropTypes.string,

	/**
	* Whether sidebar and sidebar toogle should be visible. Default: True.
	*/
	disable: PropTypes.bool,
	
	/**
	* Sidebar title.
	*/
	title: PropTypes.string,
	
	/**
	* Sidebar skin, options dark or light. Default: dark.
	*/
	skin: PropTypes.string,

	/**
	* A color for the sidebar, options: primary, secondary, success, info, 
	* warning, danger. Default: primary.
	*/
	color: PropTypes.string,
	
	/**
	* A color for the brand, options: primary, secondary, success, info, 
	* warning, danger, white or light-grey. Default: NULL.
	*/
	brand_color: PropTypes.string,

	/**
	* Sidebar brand link.
	*/
	url: PropTypes.string,

	/**
	* Sidebar brand image.
	*/
	src: PropTypes.string,

	/**
	* Sidebar opacity. From 0 to 1. Default: 0.8.
	*/
	opacity: PropTypes.number,

	/**
	* Sidebar elevation. Default: 4.
	*/
	elevation: PropTypes.number,
	
    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func
	
};